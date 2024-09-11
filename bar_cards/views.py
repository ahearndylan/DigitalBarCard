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
    # Get the BBO number from the session (or other mechanism)
    bbo_number = request.session.get('bbo_number')

    if not bbo_number:
        return HttpResponse("No BBO number found in session. Please verify the lawyer first.", status=400)

    # Encode a URL that will display the simulated card
    qr_data = f"http://127.0.0.1:8000/bar_cards/view/{bbo_number}/"

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




def generate_wallet_pass(request):
    # Fetch the lawyer's BBO number from the session (or from a form submission)
    bbo_number = request.session.get('bbo_number')

    if not bbo_number:
        return HttpResponse("No BBO number found in session. Please verify the lawyer first.", status=400)

    # Fetch lawyer details from the mock API (replace with actual API when available)
    response = requests.get(f'http://127.0.0.1:8000/mockapi/verify_bbo/{bbo_number}/')
    
    if response.status_code == 200:
        lawyer = response.json()

        # Dynamically create pass.json with the API data
        pass_data = {
            "formatVersion": 1,
            "passTypeIdentifier": "pass.com.yourorganization.barcard",
            "serialNumber": lawyer['bbo_number'],
            "teamIdentifier": "TEAMID",  # Replace with your Apple team ID
            "backgroundColor": "rgb(255,255,255)",
            "labelColor": "rgb(0,0,0)",
            "foregroundColor": "rgb(0,0,0)",
            "organizationName": "Massachusetts Board of Bar Overseers",
            "description": "Lawyer Bar Card",
            "barcode": {
                "message": f"BBO: {lawyer['bbo_number']}",
                "format": "PKBarcodeFormatQR",
                "messageEncoding": "iso-8859-1"
            },
            "generic": {
                "primaryFields": [
                    {"key": "name", "label": "Lawyer Name", "value": lawyer['name']}
                ],
                "secondaryFields": [
                    {"key": "bbo_number", "label": "BBO Number", "value": lawyer['bbo_number']},
                    {"key": "admittance_date", "label": "Admittance Date", "value": lawyer.get('admittance_date', 'N/A')},
                    {"key": "expiration_date", "label": "Expiration Date", "value": lawyer.get('expiration_date', 'N/A')}
                ],
                "auxiliaryFields": [
                    {"key": "law_firm", "label": "Law Firm", "value": lawyer.get('law_firm', 'N/A')},
                    {"key": "address", "label": "Address", "value": lawyer.get('address', 'N/A')}
                ]
            }
        }

        # Create the pass.json file
        pass_json_path = "/path/to/save/pass.json"  # Update this path
        with open(pass_json_path, 'w') as f:
            json.dump(pass_data, f)

        # Create the .pkpass file (ZIP)
        pkpass_path = "/path/to/save/pass.pkpass"  # Update this path
        with zipfile.ZipFile(pkpass_path, 'w') as pass_file:
            pass_file.write(pass_json_path, "pass.json")
            # Add logo and other images here
            # pass_file.write("/path/to/logo.png", "logo.png")

        # Send the .pkpass file as a response
        with open(pkpass_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type="application/vnd.apple.pkpass")
            response['Content-Disposition'] = f'attachment; filename=bar_card_{bbo_number}.pkpass'
            return response
    else:
        return HttpResponse(f"Could not retrieve lawyer data: {response.status_code}", status=500)