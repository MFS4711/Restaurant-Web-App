from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from datetime import datetime, timedelta
from django.utils import timezone
from decimal import Decimal

from .models import Table, Booking


class TableModelTest(TestCase):

    def setUp(self):
        """
        Set up a test instance of Table to be used in the following test cases.

        This method creates a `Table` object that will be available for all test methods.
        """
        self.table = Table.objects.create(
            table_number="A1",
            capacity=4,
            is_available=True
        )

    def test_table_creation(self):
        """
        Test that a Table object is correctly created and its fields 
        match the given data.
        """
        self.assertEqual(self.table.table_number, "A1")
        self.assertEqual(self.table.capacity, 4)
        self.assertTrue(self.table.is_available)

    def test_table_str_method(self):
        """
        Test the `__str__` method of the Table model.

        The `__str__` method should return a string representation of the Table 
        based on the table number and its capacity.
        """
        self.assertEqual(str(self.table), "Table A1 --- 4 seats")

    def test_default_availability(self):
        """
        Test the default availability of a newly created table.
        """
        new_table = Table.objects.create(
            table_number="B2",
            capacity=2
        )
        self.assertTrue(new_table.is_available)


class BookingModelTest(TestCase):

    def setUp(self):
        """
        Set up test instances of User, Table, and Booking for the following test cases.
        """
        self.user = User.objects.create_user(
            username="testuser", password="password")
        self.table = Table.objects.create(
            table_number="A1",
            capacity=4,
            is_available=True
        )
        self.booking = Booking.objects.create(
            user=self.user,
            date=timezone.now().date(),
            time=timezone.now().time(),
            number_of_people=4,
            table=self.table,
            status=Booking.PENDING
        )

    def test_booking_creation(self):
        """
        Test that a Booking object is correctly created and its fields
        match the given data.
        """
        # Remove microseconds from the time to avoid comparison issues
        booking_time = self.booking.time.replace(
            microsecond=0)  # Remove microseconds
        current_time = timezone.now().time().replace(
            microsecond=0)  # Remove microseconds

        # Check that all fields of the booking are correct
        self.assertEqual(self.booking.user.username, "testuser")
        self.assertEqual(self.booking.date, timezone.now().date())
        # Compare time without microseconds
        self.assertEqual(booking_time, current_time)
        self.assertEqual(self.booking.number_of_people, 4)
        self.assertEqual(self.booking.table.table_number, "A1")
        self.assertEqual(self.booking.status, Booking.PENDING)

    def test_get_end_time(self):
        """
        Test the `get_end_time` method of the Booking model.

        This should return the correct end time, assuming a 2-hour duration.
        """
        expected_end_time = timezone.make_aware(
            datetime.combine(self.booking.date,
                                self.booking.time) + timedelta(hours=2)
        )
        self.assertEqual(self.booking.get_end_time(), expected_end_time)

    def test_booking_str_method(self):
        """
        Test the `__str__` method of the Booking model.

        The `__str__` method should return a string representation of the booking 
        including the booking ID, user, date, and time.
        """
        self.assertEqual(str(self.booking),
        f"Booking {self.booking.id} by testuser on {self.booking.date} at {self.booking.time}")

    def test_booking_status_choices(self):
        """
        Test that the `status` field of the Booking model is limited to the defined choices.
        """
        valid_statuses = [choice[0] for choice in Booking.STATUS_CHOICES]
        self.assertIn(self.booking.status, valid_statuses)

    def test_cancelled_booking_clears_table(self):
        """
        Test that when a booking is cancelled, the associated table is cleared.
        """
        self.booking.status = Booking.CANCELLED
        self.booking.save()
        self.booking.refresh_from_db()
        self.assertIsNone(self.booking.table)

    def test_unique_booking_constraint(self):
        """
        Test that two bookings cannot occupy the same table at the same time.
        """
        # Create a new booking for the same table at the same time
        conflicting_booking = Booking(
            user=self.user,
            date=self.booking.date,
            time=self.booking.time,
            number_of_people=4,
            table=self.table,
            status=Booking.PENDING
        )

        # Expect a IntegrityError due to the unique constraint
        with self.assertRaises(Exception):
            conflicting_booking.save()

    def test_table_availability_check(self):
        """
        Test that a booking cannot be created for a table that is not available.
        """
        # Mark the table as unavailable
        self.table.is_available = False
        self.table.save()

        # Try creating a booking for the unavailable table
        unavailable_booking = Booking(
            user=self.user,
            date=timezone.now().date(),
            time=timezone.now().time(),
            number_of_people=4,
            table=self.table,
            status=Booking.PENDING
        )

        # Check that a ValueError is raised
        with self.assertRaises(ValueError):
            unavailable_booking.save()