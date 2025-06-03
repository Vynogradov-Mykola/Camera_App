from django.test import TestCase
from cameras.views import train_motion_classifier
import numpy as np


class MotionDetectionTests(TestCase):
    def test_classifier_predicts_motion(self):
        model, scaler = train_motion_classifier()

        # Значення, які явно повинні класифікуватися як "є рух"
        motion_areas = [[1_000_000], [1_500_000]]

        for area in motion_areas:
            scaled = scaler.transform([area])
            prediction = model.predict(scaled)
            self.assertEqual(prediction[0], 1, f"Expected motion for area {area}")

    def test_classifier_predicts_no_motion(self):
        model, scaler = train_motion_classifier()

        # Значення, які повинні бути класифіковані як "нема руху"
        motion_areas = [[0], [50_000]]

        for area in motion_areas:
            scaled = scaler.transform([area])
            prediction = model.predict(scaled)
            self.assertEqual(prediction[0], 0, f"Expected no motion for area {area}")
