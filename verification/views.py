from django.shortcuts import render
from django.http import JsonResponse
import requests

def verify_lawyer_form(request):
    return render(request, 'verifyLawyer.html')

def verify_lawyer_by_name(request, first_name, last_name):
    url = f"https://mockapi-xlku.onrender.com/verify_name/{first_name}/{last_name}/"
    response = requests.get(url)
    
    if response.status_code == 200:
        lawyer = response.json()
        if lawyer['public_discipline']:
            return JsonResponse({'status': 'unverified', 'error': 'Public discipline issue'})
        if not lawyer['dues_paid']:
            return JsonResponse({'status': 'unverified', 'error': 'Unpaid dues'})
        
        request.session['bbo_number'] = lawyer['bbo_number']
        return JsonResponse({'status': 'verified', 'name': f"Attorney {lawyer['name']}", 'status_message': 'Active'})
    
    return JsonResponse({'status': 'unverified', 'error': 'Lawyer not found'})

def verify_lawyer_by_bbo(request, bbo_number):
    url = f"https://mockapi-xlku.onrender.com/verify_bbo/{bbo_number}/"
    response = requests.get(url)
    
    if response.status_code == 200:
        lawyer = response.json()
        if lawyer['public_discipline']:
            return JsonResponse({'status': 'unverified', 'error': 'Public discipline issue'})
        if not lawyer['dues_paid']:
            return JsonResponse({'status': 'unverified', 'error': 'Unpaid dues'})
        
        request.session['bbo_number'] = lawyer['bbo_number']
        return JsonResponse({'status': 'verified', 'name': f"Attorney {lawyer['name']}", 'status_message': 'Active'})
    
    return JsonResponse({'status': 'unverified', 'error': 'Lawyer not found'})
