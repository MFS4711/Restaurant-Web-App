from django.shortcuts import render

# Create your views here.
def homepage(request):
    """
    Display the homepage.

    **Context:**

    None

    **Template:**

    :template:`menu/index.html`
    """
    return render(request, "core/index.html")


def contact(request):
    """

    """
    return render(request, "core/contact.html")
