from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.db import transaction
from Gestionnaires.models import Gestionnaire
from .forms import EmployeRegistrationForm
import logging

logger = logging.getLogger(__name__)

def employe_registration_view(request):
    success_message = None
    username = None

    if request.method == 'POST':
        form = EmployeRegistrationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Save the user
                    user = form.save()
                    logger.info(f"User created: {user.username}")

                    # Assign to group Gestionnaire
                    gestionnaire_group, created = Group.objects.get_or_create(name="Gestionnaire")
                    user.groups.add(gestionnaire_group)
                    logger.info(f"User {user.username} added to Gestionnaire group")

                    # Create Gestionnaire profile
                    gestionnaire = Gestionnaire.objects.create(user=user)
                    gestionnaire.save()
                    logger.info(f"Gestionnaire profile created for {user.username}")

                    success_message = f"Le compte a été créé avec succès pour l'utilisateur : {user.username}"
                    username = user.username
                    
            except Exception as e:
                logger.error(f"Error creating gestionnaire: {str(e)}")
                form.add_error(None, f"Erreur lors de la création du compte: {str(e)}")
        else:
            logger.error(f"Form validation errors: {form.errors}")
    else:
        form = EmployeRegistrationForm()

    return render(
        request,
        'employe_registration.html',
        {
            'form': form,
            'success_message': success_message,
            'username': username
        }
    )