from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from booking.models import Table, Booking
from booking.utils import generate_time_slots, is_table_available, generate_conflicting_time_range, get_table_availability_for_day

# Create your views here.

@login_required
def customer_dashboard(request, user_id):
    """

    """
    # Check if the logged-in user is the same as the user_id in the URL
    if request.user.id != int(user_id):
        # If they are not the same, redirect to a different page, for example, a 404 or the homepage
        raise Http404("You are not authorized to view this page.")
    
    user = get_object_or_404(User, id=user_id)

    # Get current date and time for comparisons
    current_time = timezone.now()

    # Fetch upcoming bookings (bookings that are in the future)
    upcoming_bookings = Booking.objects.filter(user=user, date__gte=current_time.date(
    ), time__gte=current_time.time(), status__in=['confirmed', 'pending']).order_by('date', 'time')

    # Fetch past bookings (bookings that are in the past)
    past_bookings = Booking.objects.filter(user=user, date__lt=current_time.date(
    ), status='completed').order_by('-date', '-time')

    # Fetch customer action required bookings (status 'customer_confirmation_required')
    customer_action_required_bookings = Booking.objects.filter(
        user=user, status=Booking.CUSTOMER_CONFIRMATION_REQUIRED).order_by('date', 'time')

    context = {
        'user': user,
        'upcoming_bookings': upcoming_bookings,
        'past_bookings': past_bookings,
        'customer_action_required_bookings': customer_action_required_bookings,
    }

    return render(request, 'dashboard/customer_dashboard.html', context)

# Custom decorator to check if the user is a staff member
def is_staff(user):
    return user.is_staff

@login_required(login_url='/login/')  # redirect to login page if not authenticated
@user_passes_test(is_staff, login_url='/unauthorized/')
def staff_dashboard(request):
    """

    """
    # Use the utility function to generate time slots with dynamic opening hours
    time_slots = generate_time_slots(interval_minutes=15)

    # Get today's date
    today = timezone.now().date()

    # Get table availability using the utility function
    table_availability = get_table_availability_for_day(today, time_slots)

    # Fetch bookings for today (Confirmed and Pending)
    today_bookings = Booking.objects.filter(
        date=today, status__in=[Booking.CONFIRMED]
    ).order_by('time')

    # Pass data to the context
    context = {
        'time_slots': time_slots,
        'table_availability': table_availability,
        'today': today,
        'today_bookings': today_bookings,
    }

    return render(request, 'dashboard/staff_dashboard.html', context)


# Custom decorator to check if the user is a staff member
def is_superuser(user):
    return user.is_superuser


@login_required(login_url='/login/')  # redirect to login page if not authenticated
@user_passes_test(is_superuser, login_url='/unauthorized/')
def admin_dashboard(request):
    """

    """
    # Use the utility function to generate time slots with dynamic opening hours
    time_slots = generate_time_slots(interval_minutes=15)

    # Get today's date
    today = timezone.now().date()

    # Get table availability using the utility function
    table_availability = get_table_availability_for_day(today, time_slots)

    # Fetch bookings for today (Confirmed and Pending)
    today_bookings = Booking.objects.filter(
        date=today, status__in=[Booking.CONFIRMED]
    ).order_by('time')

    # Pass data to the context
    context = {
        'time_slots': time_slots,
        'table_availability': table_availability,
        'today': today,
        'today_bookings': today_bookings,
    }

    return render(request, 'dashboard/admin_dashboard.html', context)