from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.db import IntegrityError
from .models import Table, Booking
from .forms import BookingForm, StaffBookingForm, CustomerConfirmationForm
from .utils import generate_time_slots, get_table_availability_for_day

# Custom decorator to check if the user is a staff member


def is_staff(user):
    """
    Check if the user is a staff member.

    **Context:**

    ``user``
        The user to be checked.

    **Returns:**
        True if the user is a staff member, False otherwise.
    """
    return user.is_staff


def book_table(request):
    """
    Handle table booking by users (authenticated or guest).

    **Context:**

    ``booking_form``
        An instance of :form:`BookingForm` to create a new booking.

    **Template:**

    :template:`booking/booking.html`
    """
    if request.method == 'POST':
        booking_form = BookingForm(request.POST)
        if booking_form.is_valid():
            # Save the booking without committing to the database yet
            booking = booking_form.save(commit=False)

            # If the user is logged in, assign the user to the booking
            if request.user.is_authenticated:
                booking.user = request.user
            else:
                # Allow booking for guests/non-logged in users if permitted
                pass

            # Save the booking to the database
            booking.save()

            # Redirect to the booking success page
            return redirect('booking_success', booking_id=booking.id)

    else:
        # Display the empty form for booking
        booking_form = BookingForm()

    context = {
        'booking_form': booking_form
    }

    # Render the booking page with the context data
    return render(request, "booking/booking.html", context)


@login_required(login_url='/login/')
def booking_success(request, booking_id):
    """
    Display the booking success page.

    This view handles the successful booking page, where the user is shown
    the details of their booking after a successful table reservation. The
    booking can either belongto the logged-in user or a staff member.

    **Template:**

    :template:`booking/booking_success.html`

    **Context:**

    ``booking``
        The booking object that was successfully made
        and is being displayed to the user.

    **Authorization:**

    The user must be either the owner of the booking (i.e., the user who
    created the booking) or a staff member to access this page. If the user
    does not have the necessary permission, they are redirected to the customer
    dashboard with an error message.

    """
    # Fetch the booking object first
    booking = get_object_or_404(Booking, id=booking_id)

    # Check if the user is authorized to view the booking
    if request.user != booking.user and not request.user.is_staff:
        messages.error(request, "This is not your booking.")
        return redirect('customer_dashboard', user_id=request.user.id)

    context = {
        'booking': booking,
    }

    return render(request, 'booking/booking_success.html', context)


# Redirect to login page if not authenticated
@login_required(login_url='/login/')
@user_passes_test(is_staff, login_url='/unauthorized/')
def manage_bookings(request):
    """
    Display and manage all bookings, categorized by status.

    **Context:**

    ``pending_bookings``
        A queryset of bookings that are pending and not yet assigned to tables.

    ``confirmed_bookings``
        A queryset of confirmed bookings sorted by date and time.

    ``confirmed_bookings_with_table``
        A queryset of confirmed bookings that are assigned a table.

    ``cancelled_bookings``
        A queryset of cancelled bookings.

    ``completed_bookings``
        A queryset of completed bookings.

    ``no_show_bookings``
        A queryset of no-show bookings.

    ``customer_confirmation_required_bookings``
        A queryset of bookings that require customer confirmation.

    **Template:**

    :template:`booking/manage_bookings.html`
    """
    confirmed_bookings = Booking.objects.filter(
        status=Booking.CONFIRMED).order_by('date', 'time')

    # Check for expired confirmed bookings and mark them as 'No Show'
    for booking in confirmed_bookings:
        end_time = booking.get_end_time()
        if end_time <= timezone.now():
            booking.status = Booking.NO_SHOW
            booking.save()

    # Get the list of bookings for various statuses
    pending_bookings = Booking.objects.filter(
        status=Booking.PENDING, table__isnull=True).order_by('date', 'time')
    confirmed_bookings_with_table = Booking.objects.filter(
        status=Booking.CONFIRMED
    ).exclude(
        table__isnull=True
    ).order_by(
        'date', 'time'
    )
    cancelled_bookings = Booking.objects.filter(
        status=Booking.CANCELLED).order_by('date', 'time')
    completed_bookings = Booking.objects.filter(
        status=Booking.COMPLETED).order_by('date', 'time')
    no_show_bookings = Booking.objects.filter(
        status=Booking.NO_SHOW).order_by('date', 'time')
    customer_confirmation_required_bookings = Booking.objects.filter(
        status=Booking.CUSTOMER_CONFIRMATION_REQUIRED).order_by('date', 'time')

    # Pass the bookings to the context
    context = {
        'pending_bookings': pending_bookings,
        'confirmed_bookings': confirmed_bookings,
        'confirmed_bookings_with_table': confirmed_bookings_with_table,
        'cancelled_bookings': cancelled_bookings,
        'completed_bookings': completed_bookings,
        'no_show_bookings': no_show_bookings,
        'customer_confirmation_required_bookings': (
            customer_confirmation_required_bookings
        ),
    }

    # Render the manage bookings page with the context data
    return render(request, 'booking/manage_bookings.html', context)


def edit_booking(request, booking_id):
    """
    Edit an existing booking based on the user's role (customer or staff).

    **Context:**

    ``booking_form``
        An instance of :form:`BookingForm` for customers
        or :form:`StaffBookingForm` for staff.

    ``booking``
        The booking instance being edited.

    ``is_customer``
        A flag indicating if the user is a customer (True) or staff (False).

    ``time_slots``
        A list of available time slots for staff to select from.

    ``table_availability``
        A dictionary containing available tables and their time slots for staff

    **Template:**

    :template:`booking/edit_booking.html`
    """
    booking = get_object_or_404(Booking, id=booking_id)

    # Check if the user is authorized to edit the booking
    if request.user != booking.user and not request.user.is_staff:
        messages.error(request, "You cannot edit this booking.")
        return redirect('customer_dashboard', user_id=request.user.id)

    # If the user is the customer who made the booking
    if not request.user.is_staff and request.user == booking.user:
        if booking.status == Booking.CUSTOMER_CONFIRMATION_REQUIRED:
            if request.method == 'POST':
                customer_confirmation_form = CustomerConfirmationForm(
                    request.POST, instance=booking)
                if customer_confirmation_form.is_valid():
                    customer_confirmation_form.save()
                    messages.success(
                        request, "Your booking status has been updated.")
                    return redirect(
                        'customer_dashboard',
                        user_id=request.user.id
                    )
            else:
                customer_confirmation_form = CustomerConfirmationForm(
                    instance=booking)

            # Render the form for customer confirmation
            context = {
                'booking_form': customer_confirmation_form,
                'booking': booking,
                'is_customer': True,
            }
            return render(request, 'booking/edit_booking.html', context)

        # Handle regular customer booking updates
        if request.method == 'POST':
            booking_form = BookingForm(request.POST, instance=booking)
            if booking_form.is_valid():
                updated_booking = booking_form.save(commit=False)
                # Ensure the booking status is set to PENDING if it's not
                if updated_booking.status != Booking.PENDING:
                    updated_booking.status = Booking.PENDING
                    updated_booking.table = None
                updated_booking.save()
                messages.success(
                    request, "Your booking has been updated successfully.")
                return redirect('customer_dashboard', user_id=request.user.id)
        else:
            booking_form = BookingForm(instance=booking)

        # Render the form for editing a customer booking
        context = {
            'booking_form': booking_form,
            'booking': booking,
            'is_customer': True,
        }
        return render(request, 'booking/edit_booking.html', context)

    # Handle staff's ability to edit the booking
    if request.user.is_staff:
        # Generate time slots and check table availability
        time_slots = generate_time_slots(interval_minutes=15)
        booking_date = booking.date
        table_availability = get_table_availability_for_day(
            booking_date, time_slots)

        # Handle POST request for staff updating booking
        if request.method == 'POST':
            staff_form = StaffBookingForm(request.POST, instance=booking)
            if staff_form.is_valid():
                updated_booking = staff_form.save(commit=False)

                try:
                    updated_booking.save()
                    messages.success(request, "Booking updated successfully.")
                    return redirect('manage_bookings')
                except IntegrityError:
                    messages.error(
                        request, "This table is already booked for the \
                        selected date and time. Please choose another table.")
                    return redirect('edit_booking', booking_id=booking.id)
                except Exception as e:
                    messages.error(
                        request, f"An unexpected error occurred: {str(e)}")
                    return redirect('edit_booking', booking_id=booking.id)
            else:
                # If the form is not valid, show form errors as messages
                for field, errors in staff_form.errors.items():
                    for error in errors:
                        messages.error(
                            request, f"{field.capitalize()}: {error}")
        else:
            staff_form = StaffBookingForm(
                instance=booking,
                initial={'number_of_people': booking.number_of_people}
            )

        # Render the form for staff to edit a booking
        context = {
            'staff_form': staff_form,
            'booking': booking,
            'is_customer': False,
            'time_slots': time_slots,
            'table_availability': table_availability,
        }
        return render(request, 'booking/edit_booking.html', context)


def delete_booking(request, booking_id):
    """
    Delete an existing booking.

    **Context:**

    None

    **Template:**

    :template:`booking/booking_success.html`
    """
    booking = get_object_or_404(Booking, pk=booking_id)

    # Check if the user has permission to delete the booking
    if booking.user == request.user or request.user.is_staff:
        booking.delete()
        messages.add_message(request, messages.SUCCESS,
                             'Booking successfully deleted!')
    else:
        messages.add_message(
            request, messages.ERROR, 'You do not have permission \
            to delete this booking.')

    # Redirect to the appropriate page after deletion
    if request.user.is_staff:
        return redirect('manage_bookings')

    return redirect('customer_dashboard', user_id=request.user.id)
