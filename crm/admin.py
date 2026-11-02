from django.contrib import admin
from .models import Customer, Lead, Activity


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'company', 'created_at')
    search_fields = ('name', 'email', 'company', 'phone')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'source', 'status', 'customer', 'created_at')
    list_filter = ('status', 'source', 'created_at')
    search_fields = ('name', 'email', 'phone', 'notes')
    ordering = ('-created_at',)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('activity_type', 'subject', 'customer', 'lead', 'date', 'created_by')
    list_filter = ('activity_type', 'date')
    search_fields = ('subject', 'notes', 'customer__name', 'lead__name')
    ordering = ('-date',)
