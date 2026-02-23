from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from .models import Room, Booking


class WorkingHoursValidationTest(APITestCase):
    def setUp(self):
        self.room = Room.objects.create(
            name="Переговорная 1",
            capacity=10,
            has_projector=True
        )

    def _make_datetime(self, hour, minute=0):
        tomorrow = timezone.now().date() + timedelta(days=1)
        return timezone.make_aware(
            timezone.datetime(tomorrow.year, tomorrow.month, tomorrow.day, hour, minute)
        )

    def test_booking_within_working_hours_success(self):
        response = self.client.post('/bookings/', {
            'room': self.room.id,
            'user_name': 'Иван Иванов',
            'start_time': self._make_datetime(9, 0).isoformat(),
            'end_time': self._make_datetime(10, 0).isoformat(),
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_booking_at_end_of_working_hours_success(self):
        response = self.client.post('/bookings/', {
            'room': self.room.id,
            'user_name': 'Петр Петров',
            'start_time': self._make_datetime(17, 0).isoformat(),
            'end_time': self._make_datetime(18, 0).isoformat(),
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_booking_before_working_hours_fails(self):
        response = self.client.post('/bookings/', {
            'room': self.room.id,
            'user_name': 'Иван Иванов',
            'start_time': self._make_datetime(8, 0).isoformat(),
            'end_time': self._make_datetime(9, 0).isoformat(),
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('рабочие часы', str(response.data).lower())

    def test_booking_after_working_hours_fails(self):
        response = self.client.post('/bookings/', {
            'room': self.room.id,
            'user_name': 'Иван Иванов',
            'start_time': self._make_datetime(18, 0).isoformat(),
            'end_time': self._make_datetime(19, 0).isoformat(),
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('рабочие часы', str(response.data).lower())

    def test_booking_end_time_after_working_hours_fails(self):
        response = self.client.post('/bookings/', {
            'room': self.room.id,
            'user_name': 'Иван Иванов',
            'start_time': self._make_datetime(17, 0).isoformat(),
            'end_time': self._make_datetime(18, 30).isoformat(),
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('рабочие часы', str(response.data).lower())
