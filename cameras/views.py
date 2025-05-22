from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Camera

def camera_list(request):
    cameras = Camera.objects.all()
    return render(request, 'cameras/camera_list.html', {'cameras': cameras})


from django.http import StreamingHttpResponse
from django.shortcuts import render
import cv2

def gen(camera):
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Кодуємо у формат JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # Створюємо потік
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def video_feed(request):
    return StreamingHttpResponse(gen(cv2.VideoCapture(0)),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


def camera_stream(request):
    return render(request, 'cameras/camera_stream.html')
