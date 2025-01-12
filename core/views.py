from django.shortcuts import render
from django.contrib import messages
# Create your views here.


def homepage(request):
    """
    Display the homepage.

    **Context:**

    None

    **Template:**

    :template:`core/index.html`
    """
    if request.user.is_authenticated:
        # Add a success message if the user is logged in
        messages.success(
            request,
            f"You are logged in as {request.user.username}."
        )

    else:
        # Add an error message if the user is not logged in
        messages.info(request, "You are currently not logged in.")

    return render(request, "core/index.html")


def contact(request):
    """
    Display the contact page.

    **Context:**

    None

    **Template:**

    :template:`core/contact.html`
    """
    return render(request, "core/contact.html")
