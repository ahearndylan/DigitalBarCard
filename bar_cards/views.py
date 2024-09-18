from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from datetime import datetime, timedelta
import qrcode
from io import BytesIO
import requests

def view_bar_card(request):
    bbo_number = request.session.get('bbo_number')

    if not bbo_number:
        return HttpResponse("No BBO number found in session. Please validate a lawyer first.", status=400)

    response = requests.get(f'https://mockapi-xlku.onrender.com/verify_bbo/{bbo_number}/')

    if response.status_code == 200:
        lawyer = response.json()
        expiration_date = (datetime.now() + timedelta(days=365)).strftime('%m/%d/%Y')

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
    bbo_number = request.session.get('bbo_number')

    if not bbo_number:
        return HttpResponse("No BBO number found in session. Please verify the lawyer first.", status=400)

    qr_data = f"https://mockapi-xlku.onrender.com/bar_cards/display/{bbo_number}/"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img_io = BytesIO()
    img.save(img_io, format='PNG')
    img_io.seek(0)

    return HttpResponse(img_io, content_type='image/png')


def bar_card_display(request, bbo_number):
    response = requests.get(f'https://mockapi-xlku.onrender.com/verify_bbo/{bbo_number}/')

    if response.status_code == 200:
        lawyer = response.json()
        expiration_date = (datetime.now() + timedelta(days=365)).strftime('%m/%d/%Y')

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
