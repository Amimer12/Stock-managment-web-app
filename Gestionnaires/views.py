from django.shortcuts import render
from django.http import JsonResponse



def check_user_is_employee(request):
    is_employee = True
    if not request.user.groups.filter(name='Gestionnaire').exists():
        is_employee = False
    return JsonResponse({'is_employee': is_employee})
