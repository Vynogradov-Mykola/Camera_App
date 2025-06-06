from django.shortcuts import render
from django.urls import reverse
from django.http import StreamingHttpResponse, JsonResponse
from .models import Camera
from .mongo_utils import insert_series, get_all_series, get_series_by_name, insert_motion_event, get_all_motion_events
from datetime import datetime
import cv2
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import json


def camera_list(request):
    cameras = Camera.objects.all()
    for cam in cameras:
        cam.stream_url = request.build_absolute_uri(reverse('camera_stream'))
    return render(request, 'cameras/camera_list.html', {'cameras': cameras})


# Навчання простого класифікатора
def train_motion_classifier():
    X = [[0], [50000], [900000], [1200000], [1500000]]
    y = [0, 0, 1, 1, 1]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = LogisticRegression()
    model.fit(X_scaled, y)

    return model, scaler


def gen(camera):
    prev_frame = None
    font = cv2.FONT_HERSHEY_SIMPLEX
    model, scaler = train_motion_classifier()

    while True:
        success, frame = camera.read()
        if not success:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        motion_detected = False

        if prev_frame is not None:
            frame_delta = cv2.absdiff(prev_frame, gray)
            thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
            motion_area = np.sum(thresh)

            scaled_area = scaler.transform([[motion_area]])
            prediction = model.predict(scaled_area)
            motion_detected = prediction[0] == 1

            if motion_detected:
                cv2.putText(frame, "Motion detected!", (10, 30), font, 1, (0, 0, 0), 2)

                # Збереження події в MongoDB
                event_data = {
                    "timestamp": datetime.utcnow(),
                    "motion_area": int(motion_area),
                    "camera_id": "default_camera",
                    "event": "motion_detected"
                }
                insert_motion_event(event_data)

        prev_frame = gray

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def video_feed(request):
    return StreamingHttpResponse(gen(cv2.VideoCapture(0)),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


def camera_stream(request):
    return render(request, 'cameras/camera_stream.html')


def series_list_view(request):
    series = get_all_series()
    for s in series:
        s['_id'] = str(s['_id'])
    return JsonResponse(series, safe=False)


def series_add_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        inserted_id = insert_series(data)
        return JsonResponse({'inserted_id': str(inserted_id)})
    return JsonResponse({'error': 'Only POST method allowed'}, status=405)


def motion_events_view(request):
    events = get_all_motion_events()
    for e in events:
        e['_id'] = str(e['_id'])
        if 'timestamp' in e:
            e['timestamp'] = e['timestamp'].isoformat()
    return JsonResponse(events, safe=False)
