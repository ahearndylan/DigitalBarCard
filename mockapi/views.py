from django.http import JsonResponse

# Mock data simulating a real API
lawyers = [
    {
        "status": "active",
        "name": "Robert Ahearn",
        "bbo_number": "556902",
        "public_discipline": False,
        "dues_paid": True,
        "admittance_date": "12/20/1990",
        "law_firm": "Law Offices of Robert D. Ahearn, P.C.",
        "address": "15 Cottage Ave, Suite 202 Quincy, Massachusetts 02169"
    },
    {
        "status": "active",
        "name": "Ashley Ahearn",
        "bbo_number": "708891",
        "public_discipline": False,
        "dues_paid": True,
        "admittance_date": "12/14/2021",
        "law_firm": "Law Offices of Robert D. Ahearn, P.C.",
        "address": "15 Cottage Ave, Suite 202 Quincy, Massachusetts 02169"
    },
    {
        "name": "John Glynn",
        "bbo_number": "123456",
        "status": "active",
        "public_discipline": True,
        "dues_paid": True
    },
    {
        "name": "Tim Smith",
        "bbo_number": "789012",
        "status": "active",
        "public_discipline": False,
        "dues_paid": False
    }
]

def verify_lawyer_by_bbo(request, bbo_number):
    lawyer = next((lawyer for lawyer in lawyers if lawyer['bbo_number'] == bbo_number), None)
    if lawyer:
        return JsonResponse(lawyer)
    else:
        return JsonResponse({'error': 'BBO number not found'}, status=404)

def verify_lawyer_by_name(request, first_name, last_name):
    full_name = f"{first_name.capitalize()} {last_name.capitalize()}"
    lawyer = next((lawyer for lawyer in lawyers if lawyer["name"].lower() == full_name.lower()), None)
    if lawyer:
        return JsonResponse(lawyer)
    else:
        return JsonResponse({'error': 'Lawyer not found'}, status=404)
