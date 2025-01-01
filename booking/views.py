from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from .models import Table, Booking
from .forms import BookingForm, StaffBookingForm

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
    pending_bookings = Booking.objects.filter(
        status=Booking.PENDING, table__isnull=True)

    # Fetch confirmed bookings that have a table assigned
    confirmed_bookings = Booking.objects.filter(
        status=Booking.CONFIRMED).exclude(table__isnull=True)

    context = {
        'pending_bookings': pending_bookings,
        'confirmed_bookings': confirmed_bookings,
    }

    return render(request, 'booking/manage_bookings.html', context)


def edit_booking(request, booking_id):
    """

    """
    booking = get_object_or_404(Booking, id=booking_id)

    # Check if the current user is the owner of the booking (for customers)
    if request.user != booking.user and not request.user.is_staff:
        messages.error(request, "You cannot edit this booking.")
        return redirect('customer_dashboard', user_id=request.user.id)

    # If the user is a customer, use the BookingForm for them to modify their booking
    if not request.user.is_staff and request.user == booking.user:
        # Only allow customers to modify their own bookings
        if request.method == 'POST':
            booking_form = BookingForm(request.POST, instance=booking)

            if booking_form.is_valid():
                updated_booking = booking_form.save(commit=False)
                # Set the booking status to "pending" if it's not already
                if updated_booking.status != Booking.PENDING:
                    updated_booking.status = Booking.PENDING

                updated_booking.save()
                messages.success(
                    request, "Your booking has been updated successfully.")
                return redirect('customer_dashboard', user_id=request.user.id)
        else:
            # Display the booking form with pre-filled data
            booking_form = BookingForm(instance=booking)

        context = {
            'booking_form': booking_form,
            'booking': booking,
            'is_customer': True,  # Flag to indicate it's a customer edit
        }
        return render(request, 'booking/edit_booking.html', context)

    # If the user is staff, show the staff-specific form
    if request.user.is_staff:
        if request.method == 'POST':
            staff_form = StaffBookingForm(request.POST, instance=booking)
            if staff_form.is_valid():
                staff_form.save()
                messages.success(request, "Booking updated successfully.")
                return redirect('manage_bookings')
        else:
            staff_form = StaffBookingForm(instance=booking)

        context = {
            'staff_form': staff_form,
            'booking': booking,
            'is_customer': False,  # Flag to indicate it's a staff edit
        }
        return render(request, 'booking/edit_booking.html', context)
