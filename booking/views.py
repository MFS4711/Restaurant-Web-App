from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from .models import Table, Booking
from .forms import BookingForm

# Create your views here.
def book_table(request):
    """

    """

    # Display form
    booking_form = BookingForm()

    context = {
        'booking_form': booking_form
    }
    
    return render(request, "booking/booking.html", context)