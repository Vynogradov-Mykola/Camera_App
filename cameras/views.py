from django.shortcuts import render
from django.urls import reverse
from django.http import StreamingHttpResponse
from .models import Camera
import cv2
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler


def camera_list(request):
    cameras = Camera.objects.all()
    for cam in cameras:
        cam.stream_url = request.build_absolute_uri(reverse('camera_stream'))
    return render(request, 'cameras/camera_list.html', {'cameras': cameras})


# Навчання простого класифікатора
def train_motion_classifier():
    # motion_area -> клас (0: нема руху, 1: є рух)
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

            # Класифікація руху з використанням моделі
            scaled_area = scaler.transform([[motion_area]])
            prediction = model.predict(scaled_area)
            motion_detected = prediction[0] == 1

        prev_frame = gray

        if motion_detected:
            cv2.putText(frame, "Motion detected!", (10, 30), font, 1, (0, 0, 0), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def video_feed(request):
    return StreamingHttpResponse(gen(cv2.VideoCapture(0)),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


def camera_stream(request):
    return render(request, 'cameras/camera_stream.html')
