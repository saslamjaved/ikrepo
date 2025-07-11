from django.contrib import admin
from .models import CustomUser

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'phone_number', 'address','street_address','city','state','postal_code','country')
    search_fields = ('username', 'email')
    list_filter = ('user_type',)