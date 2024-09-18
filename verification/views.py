from django.shortcuts import render
from django.http import JsonResponse
import requests

# View to render the verification form
def verify_lawyer_form(request):
    return render(request, 'verifyLawyer.html')

def verify_lawyer_by_name(request, first_name, last_name):
    # Call the mock API to retrieve lawyer information by name
    url = f"http://127.0.0.1:8000/mockapi/verify_name/{first_name}/{last_name}/"
    response = requests.get(url)
    
    if response.status_code == 200:
        lawyer = response.json()
        if lawyer['public_discipline']:
            return JsonResponse({'status': 'unverified', 'error': 'Public discipline issue'})
        elif not lawyer['dues_paid']:
            return JsonResponse({'status': 'unverified', 'error': 'Unpaid dues'})
        else:
            # Store the BBO number in the session after successful verification
            request.session['bbo_number'] = lawyer['bbo_number']
            return JsonResponse({'status': 'verified', 'name': f"Attorney {lawyer['name']}", 'status_message': 'Active'})
    else:
        return JsonResponse({'status': 'unverified', 'error': 'Lawyer not found'})

# View to verify lawyer by BBO number using the mock API
def verify_lawyer_by_bbo(request, bbo_number):
    # Call the mock API to retrieve lawyer information by BBO number
    url = f"http://127.0.0.1:8000/mockapi/verify_bbo/{bbo_number}/"
    response = requests.get(url)
    
    if response.status_code == 200:
        lawyer = response.json()
        if lawyer['public_discipline']:
            return JsonResponse({'status': 'unverified', 'error': 'Public discipline issue'})
        elif not lawyer['dues_paid']:
            return JsonResponse({'status': 'unverified', 'error': 'Unpaid dues'})
        else:
            # Store the BBO number in the session after successful verification
            request.session['bbo_number'] = lawyer['bbo_number']
            return JsonResponse({'status': 'verified', 'name': f"Attorney {lawyer['name']}", 'status_message': 'Active'})
    else:
        return JsonResponse({'status': 'unverified', 'error': 'Lawyer not found'})