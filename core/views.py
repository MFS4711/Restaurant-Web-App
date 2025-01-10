from django.shortcuts import render

# Create your views here.


def homepage(request):
    """
    Display the homepage.

    **Context:**

    None

    **Template:**

    :template:`core/index.html`
    """
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
