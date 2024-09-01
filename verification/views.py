from django.shortcuts import render

# Create views here

def verify_lawyer(request):
    # Logic for verifying laywers thru BBO
    return render(request, 'bar_cards/view.html')