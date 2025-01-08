from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.utils import timezone
from django.db import IntegrityError
from .models import Table, Booking
from .forms import BookingForm, StaffBookingForm, CustomerConfirmationForm
from .utils import generate_time_slots, get_table_availability_for_day

# Create your views here.

# Custom decorator to check if the user is a staff member
def is_staff(user):
    return user.is_staff


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


@login_required(login_url='/login/')  # redirect to login page if not authenticated
@user_passes_test(is_staff, login_url='/unauthorized/')
def manage_bookings(request):
    """

    """
    # Fetch all confirmed bookings and sort them by date and time (closest first)
    confirmed_bookings = Booking.objects.filter(status=Booking.CONFIRMED).order_by('date', 'time')

    # Check if the confirmed booking's end time has passed and update status to "No Show"
    for booking in confirmed_bookings:
        end_time = booking.get_end_time()
        # If the booking's end time has passed, change its status to "No Show"
        if end_time <= timezone.now():
            booking.status = Booking.NO_SHOW
            booking.save()

    # Fetch pending bookings that do not have a table assigned and sort by date and time
    pending_bookings = Booking.objects.filter(status=Booking.PENDING, table__isnull=True).order_by('date', 'time')

    # Fetch confirmed bookings that have a table assigned and sort by date and time
    confirmed_bookings_with_table = Booking.objects.filter(status=Booking.CONFIRMED).exclude(table__isnull=True).order_by('date', 'time')

    # Fetch cancelled bookings and sort by date and time
    cancelled_bookings = Booking.objects.filter(status=Booking.CANCELLED).order_by('date', 'time')

    # Fetch completed bookings and sort by date and time
    completed_bookings = Booking.objects.filter(status=Booking.COMPLETED).order_by('date', 'time')

    # Fetch no-show bookings and sort by date and time
    no_show_bookings = Booking.objects.filter(status=Booking.NO_SHOW).order_by('date', 'time')

    # Fetch customer confirmation required bookings and sort by date and time
    customer_confirmation_required_bookings = Booking.objects.filter(
        status=Booking.CUSTOMER_CONFIRMATION_REQUIRED).order_by('date', 'time')

    context = {
        'pending_bookings': pending_bookings,
        'confirmed_bookings': confirmed_bookings,
        'confirmed_bookings_with_table': confirmed_bookings_with_table,
        'cancelled_bookings': cancelled_bookings,
        'completed_bookings': completed_bookings,
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

    # If the user is a customer, handle customer-specific logic
    if not request.user.is_staff and request.user == booking.user:
        # Check if the booking status requires customer confirmation
        if booking.status == Booking.CUSTOMER_CONFIRMATION_REQUIRED:
            # Handle customer confirmation (show only the status field)
            if request.method == 'POST':
                customer_confirmation_form = CustomerConfirmationForm(
                    request.POST, instance=booking)

                if customer_confirmation_form.is_valid():
                    customer_confirmation_form.save()
                    messages.success(request, "Your booking status has been updated.")
                    return redirect('customer_dashboard', user_id=request.user.id)
            else:
                customer_confirmation_form = CustomerConfirmationForm(instance=booking)

            context = {
                'booking_form': customer_confirmation_form,
                'booking': booking,
                'is_customer': True,  # Flag to indicate it's a customer edit
            }
            return render(request, 'booking/edit_booking.html', context)
        
        # Handle the regular booking form for customers when status is not 'Customer Confirmation Required'
        if request.method == 'POST':
            booking_form = BookingForm(request.POST, instance=booking)

            if booking_form.is_valid():
                updated_booking = booking_form.save(commit=False)
                # Set the booking status to "pending" if it's not already
                if updated_booking.status != Booking.PENDING:
                    updated_booking.status = Booking.PENDING

                updated_booking.save()
                messages.success(request, "Your booking has been updated successfully.")
                return redirect('customer_dashboard', user_id=request.user.id)
        else:
            booking_form = BookingForm(instance=booking)

        context = {
            'booking_form': booking_form,
            'booking': booking,
            'is_customer': True,  # Flag to indicate it's a customer edit
        }
        return render(request, 'booking/edit_booking.html', context)

    # If the user is staff, show the staff-specific form
    if request.user.is_staff:
        # Generate time slots for the day of the current booking
        time_slots = generate_time_slots(interval_minutes=15)
        booking_date = booking.date  # Use the current booking's date

        # Get table availability for that specific date
        table_availability = get_table_availability_for_day(booking_date, time_slots)

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
            'time_slots': time_slots,
            'table_availability': table_availability,
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
