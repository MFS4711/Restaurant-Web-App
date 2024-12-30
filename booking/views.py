from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from .models import Table, Booking

# Create your views here.
def booking(request):
    """

    """
    return render(request, "booking/booking.html")