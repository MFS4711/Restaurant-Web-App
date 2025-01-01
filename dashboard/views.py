from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.models import User
from booking.models import Table, Booking

# Create your views here.


def customer_dashboard(request, user_id):
    """

    """
    user = get_object_or_404(User, id=user_id)

    # Get current date and time for comparisons
    current_time = timezone.now()

    # Fetch upcoming bookings (bookings that are in the future)
    upcoming_bookings = Booking.objects.filter(user=user, date__gte=current_time.date(
    ), time__gte=current_time.time(), status__in=['confirmed', 'pending']).order_by('date', 'time')

    # Fetch past bookings (bookings that are in the past)
    past_bookings = Booking.objects.filter(user=user, date__lt=current_time.date(
    ), status='completed').order_by('-date', '-time')

    context = {
        'user': user,
        'upcoming_bookings': upcoming_bookings,
        'past_bookings': past_bookings
    }

    return render(request, 'dashboard/customer_dashboard.html', context)
