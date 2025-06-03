from django.test import TestCase
from cameras.views import gen
import numpy as np

class MockCamera:
    def __init__(self):
        self.frames = [np.zeros((480, 640, 3), dtype=np.uint8) for _ in range(3)]
        self.index = 0

    def read(self):
        if self.index >= len(self.frames):
            return False, None
        frame = self.frames[self.index]
        self.index += 1
        return True, frame


class GenFunctionTest(TestCase):
    def test_gen_output_format(self):
        camera = MockCamera()
        generator = gen(camera)
        frame = next(generator)
        # Перевіряємо, що відповідь має правильний формат multipart
        self.assertTrue(frame.startswith(b'--frame\r\nContent-Type: image/jpeg\r\n\r\n'))
