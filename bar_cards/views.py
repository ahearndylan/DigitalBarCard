from django.shortcuts import render

def generate_bar_card(request):
    #Logic for generating the Bar Card
    return render(request, 'bar_cards/generate.html')

def view_bar_card(request):
    #Logic for viewing the Bar Card
    return render(request, 'bar_cards/view.html')