from django.shortcuts import render
from django.http import JsonResponse
import json
from datetime import datetime, timedelta
import qrcode, os, zipfile
from io import BytesIO
from django.http import HttpResponse
import requests


def save_verified_name(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        request.session['verified_name'] = data.get('name')  # Store the name in the session
        request.session['bbo_number'] = data.get('bbo_number')  # Store BBO number in the session
        return JsonResponse({'status': 'success'})


def view_bar_card(request):
    # Get the BBO number from the session
    bbo_number = request.session.get('bbo_number')

    if not bbo_number:
        return HttpResponse("No BBO number found in session. Please validate a lawyer first.", status=400)

    # Make the request to the mock API to fetch the lawyer's data by BBO number
    response = requests.get(f'http://127.0.0.1:8000/mockapi/verify_bbo/{bbo_number}/')

    if response.status_code == 200:
        lawyer = response.json()

        # Assuming expiration date is one year from today
        creation_date = datetime.now()
        expiration_date = (creation_date + timedelta(days=365)).strftime('%m/%d/%Y')

        # Prepare the context with the lawyer's details
        context = {
            'name': lawyer['name'],
            'bbo_number': lawyer['bbo_number'],
            'admittance_date': lawyer.get('admittance_date'),
            'expiration_date': expiration_date,
            'law_firm': lawyer.get('law_firm'),
            'address': lawyer.get('address')
        }

        return render(request, 'view.html', context)
    else:
        return HttpResponse(f"Lawyer data could not be retrieved: {response.status_code}", status=500)


def generate_qr_code(request):
    # Get the BBO number from the session
    bbo_number = request.session.get('bbo_number')

    if not bbo_number:
        return HttpResponse("No BBO number found in session. Please verify the lawyer first.", status=400)

    # Use localhost (127.0.0.1) for the QR code URL
    qr_data = f"http://127.0.0.1:8000/bar_cards/display/{bbo_number}/"

    # Create the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    # Generate the QR code image
    img = qr.make_image(fill='black', back_color='white')

    # Save the image in an in-memory file
    img_io = BytesIO()
    img.save(img_io, format='PNG')
    img_io.seek(0)

    # Return the image as an HTTP response
    return HttpResponse(img_io, content_type='image/png')

def bar_card_display(request, bbo_number):
    # Retrieve lawyer details from the mock API
    response = requests.get(f'http://127.0.0.1:8000/mockapi/verify_bbo/{bbo_number}/')

    if response.status_code == 200:
        lawyer = response.json()

        # Assuming expiration date is one year from today
        creation_date = datetime.now()
        expiration_date = (creation_date + timedelta(days=365)).strftime('%m/%d/%Y')

        # Prepare the context with the lawyer's details
        context = {
            'name': lawyer['name'],
            'bbo_number': lawyer['bbo_number'],
            'admittance_date': lawyer.get('admittance_date'),
            'expiration_date': expiration_date,
            'law_firm': lawyer.get('law_firm'),
            'address': lawyer.get('address'),
            'signature': lawyer['name']
        }

        return render(request, 'bar_card.html', context)
    else:
        return HttpResponse(f"Lawyer data could not be retrieved: {response.status_code}", status=500)