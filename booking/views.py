from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from .models import Table, Booking
from .forms import BookingForm

# Create your views here.


def book_table(request):
    """

    """
    if request.method == 'POST':
        booking_form = BookingForm(request.POST)
        if booking_form.is_valid():
            booking = booking_form.save(commit=False)

            if request.user.is_authenticated:
                booking.user = request.user
            else:
                # Leave if Guest/non-logged in users are given booking permission
                pass

            booking.save()  # Save the booking

            return redirect('booking_success')  # Redirect to a success page

    else:
        # Display form
        booking_form = BookingForm()

    context = {
        'booking_form': booking_form
    }

    return render(request, "booking/booking.html", context)


def booking_success(request):
    """

    """
    return render(request, 'booking/booking_success.html')


def manage_bookings(request):
    """

    """
    # Fetch pending bookings that do not have a table assigned
    pending_bookings = Booking.objects.filter(status=Booking.PENDING, table__isnull=True)
    
    # Fetch confirmed bookings that have a table assigned
    confirmed_bookings = Booking.objects.filter(status=Booking.CONFIRMED).exclude(table__isnull=True)

    context = {
        'pending_bookings': pending_bookings,
        'confirmed_bookings': confirmed_bookings,
    }

    return render(request, 'booking/manage_bookings.html', context)