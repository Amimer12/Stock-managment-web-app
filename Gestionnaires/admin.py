from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Gestionnaire
from .forms import GestionnaireCreationForm, GestionnaireChangeForm

User = get_user_model()

@admin.register(Gestionnaire)
class GestionnaireAdmin(admin.ModelAdmin):
    add_form = GestionnaireCreationForm
    form = GestionnaireChangeForm

    list_display = (
        "get_username", "get_email", "get_first_name", "get_last_name",
        "get_is_active", "get_is_staff", "boutique_list"
    )
    search_fields = ("user__username", "user__email", "user__first_name", "user__last_name")
    list_filter = ("boutique", "user__is_active", "user__is_staff")

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            kwargs["form"] = self.add_form
        else:
            kwargs["form"] = self.form
        return super().get_form(request, obj, **kwargs)

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return [
                (None, {"fields": ("username", "email", "password1", "password2", "boutique")}),
            ]
        else:
            return [
                ("Informations utilisateur", {
                    "fields": ("username", "email", "first_name", "last_name", "is_active", "is_staff")
                }),
                ("Boutiques", {
                    "fields": ("boutique",),
                }),
            ]

    def get_username(self, obj):
        return obj.user.username if obj.user else ""
    get_username.short_description = "Nom d'utilisateur"

    def get_email(self, obj):
        return obj.user.email if obj.user else ""
    get_email.short_description = "Email"

    def get_first_name(self, obj):
        return obj.user.first_name if obj.user else ""
    get_first_name.short_description = "Prénom"

    def get_last_name(self, obj):
        return obj.user.last_name if obj.user else ""
    get_last_name.short_description = "Nom"

    def get_is_active(self, obj):
        return obj.user.is_active if obj.user else False
    get_is_active.boolean = True
    get_is_active.short_description = "Actif"

    def get_is_staff(self, obj):
        return obj.user.is_staff if obj.user else False
    get_is_staff.boolean = True
    get_is_staff.short_description = "Staff"

    def boutique_list(self, obj):
        return ", ".join([b.nom_boutique for b in obj.boutique.all()])
    boutique_list.short_description = "Boutiques"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user").prefetch_related("boutique")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        user = obj.user
        super().delete_model(request, obj)
        if user:
            user.delete()

    def delete_queryset(self, request, queryset):
        users = [obj.user for obj in queryset if obj.user]
        super().delete_queryset(request, queryset)
        User.objects.filter(pk__in=[user.pk for user in users if user]).delete()

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class CustomUserAdmin(BaseUserAdmin):
    gestionnaire_editable_fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def is_gestionnaire(self, request):
        return request.user.groups.filter(name='Gestionnaire').exists()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if self.is_gestionnaire(request):
            return qs.filter(pk=request.user.pk)
        return qs

    def get_fieldsets(self, request, obj=None):
        if self.is_gestionnaire(request):
            return [
                (None, {'fields': ('username', 'password')}),
                (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
            ]
        return super().get_fieldsets(request, obj)

    def get_readonly_fields(self, request, obj=None):
        if self.is_gestionnaire(request):
            all_fields = [f.name for f in self.model._meta.fields]
            # Make all fields readonly except allowed editable fields
            readonly = [f for f in all_fields if f not in self.gestionnaire_editable_fields]
            return readonly
        return super().get_readonly_fields(request, obj)

    def has_add_permission(self, request):
        if self.is_gestionnaire(request):
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        if self.is_gestionnaire(request):
            return False
        return super().has_delete_permission(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if self.is_gestionnaire(request):
            # Remove unwanted fields for gestionnaires
            for field_name in list(form.base_fields):
                if field_name not in self.gestionnaire_editable_fields:
                    form.base_fields.pop(field_name)
        return form

# Unregister default User admin and register the custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
