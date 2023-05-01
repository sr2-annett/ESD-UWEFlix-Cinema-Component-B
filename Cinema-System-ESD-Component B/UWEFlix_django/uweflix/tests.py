# Import necessary packages and modules
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Club, ClubRep, Customer, Film, Prices, Screen, Showing, Ticket, Transaction
from datetime import datetime, timedelta
from django.utils import timezone

class ShowingModelTestCase(TestCase):
    def setUp(self):
        film = Film.objects.create(title="Test Film", age_rating=12, duration=120,
                                    trailer_desc="Test trailer", image="test.png")
        screen = Screen.objects.create(capacity=100, apply_covid_restrictions=False)
        Showing.objects.create(film=film, screen=screen, time=timezone.make_aware(datetime(2023, 5, 1, 14, 0, 0)))

    def test_showing_str(self):
        showing = Showing.objects.get(time=timezone.make_aware(datetime(2023, 5, 1, 14, 0, 0)))
        self.assertEqual(str(showing), "Test Film - 2023-05-01 14:00:00")

    def test_delete_showing(self):
        # Create a new showing for testing purposes
        film = Film.objects.create(title="Test Film 2", age_rating=12, duration=120,
                                trailer_desc="Test trailer 2", image="test2.png")
        screen = Screen.objects.create(capacity=100, apply_covid_restrictions=False)
        showing_to_delete = Showing.objects.create(film=film, screen=screen, time=timezone.make_aware(datetime(2023, 5, 2, 14, 0, 0)))

        # Delete the showing
        showing_to_delete.delete()

        # Test that the deleted showing no longer exists
        with self.assertRaises(Showing.DoesNotExist):
            Showing.objects.get(time=timezone.make_aware(datetime(2023, 5, 2, 14, 0, 0)))

        # Test that other showings still exist
        showing = Showing.objects.get(time=timezone.make_aware(datetime(2023, 5, 1, 14, 0, 0)))
        self.assertIsNotNone(showing)
