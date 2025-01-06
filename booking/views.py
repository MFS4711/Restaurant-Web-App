from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.db import IntegrityError
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
    pending_bookings = Booking.objects.filter(status=Booking.PENDING, table__isnull=True)

    # Fetch confirmed bookings that have a table assigned
    confirmed_bookings = Booking.objects.filter(status=Booking.CONFIRMED).exclude(table__isnull=True)

    # Fetch cancelled bookings
    cancelled_bookings = Booking.objects.filter(status=Booking.CANCELLED)

    # Fetch completed bookings
    completed_bookings = Booking.objects.filter(status=Booking.COMPLETED)

    # Fetch no-show bookings
    no_show_bookings = Booking.objects.filter(status=Booking.NO_SHOW)

    # Fetch customer confirmation required bookings
    customer_confirmation_required_bookings = Booking.objects.filter(
        status=Booking.CUSTOMER_CONFIRMATION_REQUIRED)

    context = {
        'pending_bookings': pending_bookings,
        'confirmed_bookings': confirmed_bookings,
        'cancelled_bookings': cancelled_bookings,
        'completed_bookings': completed_bookings,  # Added completed bookings here
        'no_show_bookings': no_show_bookings,
        'customer_confirmation_required_bookings': customer_confirmation_required_bookings,
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
                updated_booking = staff_form.save(commit=False)

                try:
                    updated_booking.save()
                    messages.success(request, "Booking updated successfully.")
                    return redirect('manage_bookings')

                except IntegrityError:
                    # Catch duplicate booking error
                    messages.error(
                        request, "This table is already booked for the selected date and time. Please choose another table.")
                    return redirect('edit_booking', booking_id=booking.id)
                except Exception as e:
                    # Catch any unexpected errors
                    messages.error(
                        request, f"An unexpected error occurred: {str(e)}")
                    return redirect('edit_booking', booking_id=booking.id)
        else:
            # Pass the number_of_people to the form's initial data to filter the tables accordingly
            staff_form = StaffBookingForm(instance=booking, initial={
                                          'number_of_people': booking.number_of_people})

        context = {
            'staff_form': staff_form,
            'booking': booking,
            'is_customer': False,  # Flag to indicate it's a staff edit
        }
        return render(request, 'booking/edit_booking.html', context)


def delete_booking(request, booking_id):
    """

    """
    # Get the booking object you want to delete
    booking = get_object_or_404(Booking, pk=booking_id)

    # Check if the user is the one who made the booking or if the user is a staff member
    if booking.user == request.user or request.user.is_staff:
        # Delete the booking
        booking.delete()
        messages.add_message(request, messages.SUCCESS,
                             'Booking successfully deleted!')
    else:
        messages.add_message(
            request, messages.ERROR, 'You do not have permission to delete this booking.')

    # Redirect the user to the appropriate page based on their role (staff or customer)
    if request.user.is_staff:
        # Redirect staff to the manage bookings page
        return redirect('manage_bookings')
    # Redirect customer to their dashboard
    return redirect('customer_dashboard', user_id=request.user.id)
