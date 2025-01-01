from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from booking.models import Table, Booking

# Create your views here.

def customer_dashboard(request, user_id):
    """

    """
    # Fetch the user by user_id
    user = get_object_or_404(User, id=user_id)


    # Context to pass to the template
    context = {
        "user": user,
    }

    # Render the dashboard page for the specific user
    return render(request, "dashboard/customer_dashboard.html", context)
