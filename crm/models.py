from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Customer(models.Model):
    """
    Customer Model:
    Stores profile and contact information for an individual or business client.
    """
    name = models.CharField(max_length=150, verbose_name="Full Name")
    email = models.EmailField(unique=True, verbose_name="Email Address")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Phone Number")
    company = models.CharField(max_length=150, blank=True, verbose_name="Company Name")
    address = models.TextField(blank=True, verbose_name="Address")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date Added")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        if self.company:
            return f"{self.name} ({self.company})"
        return self.name

    @property
    def total_leads(self):
        return self.leads.count()

    @property
    def total_activities(self):
        return self.activities.count()


class Lead(models.Model):
    """
    Lead Model:
    Represents a potential customer or sales opportunity.
    Tracks pipeline status from Initial Contact to Conversion or Loss.
    """
    STATUS_CHOICES = [
        ('New', 'New'),
        ('Contacted', 'Contacted'),
        ('Interested', 'Interested'),
        ('Converted', 'Converted'),
        ('Lost', 'Lost'),
    ]

    SOURCE_CHOICES = [
        ('Website', 'Website / Contact Form'),
        ('Referral', 'Referral / Recommendation'),
        ('Social Media', 'Social Media'),
        ('Cold Call', 'Cold Call / Outreach'),
        ('Email Campaign', 'Email Campaign'),
        ('Event', 'Event / Conference'),
        ('Other', 'Other'),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='leads',
        help_text="Optional: Link this lead to an existing customer record."
    )
    name = models.CharField(max_length=150, verbose_name="Customer / Contact Name")
    email = models.EmailField(verbose_name="Email Address")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Phone Number")
    source = models.CharField(
        max_length=50,
        choices=SOURCE_CHOICES,
        default='Website',
        verbose_name="Lead Source"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='New',
        verbose_name="Lead Status"
    )
    notes = models.TextField(blank=True, verbose_name="Notes")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Lead"
        verbose_name_plural = "Leads"

    def __str__(self):
        return f"{self.name} - [{self.status}]"

    @property
    def status_badge_class(self):
        """Returns the appropriate Bootstrap 5 badge class for this lead status."""
        badge_map = {
            'New': 'bg-secondary',
            'Contacted': 'bg-info text-dark',
            'Interested': 'bg-warning text-dark',
            'Converted': 'bg-success',
            'Lost': 'bg-danger',
        }
        return badge_map.get(self.status, 'bg-secondary')


class Activity(models.Model):
    """
    Activity Model:
    Logs every interaction (phone call, meeting, email, note) with a customer.
    Linked to Customer (required) and optionally to a Lead.
    """
    ACTIVITY_TYPE_CHOICES = [
        ('Call', 'Phone Call'),
        ('Meeting', 'Meeting'),
        ('Email', 'Email'),
        ('Note', 'General Note'),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='activities',
        verbose_name="Customer"
    )
    lead = models.ForeignKey(
        Lead,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='activities',
        verbose_name="Related Lead"
    )
    activity_type = models.CharField(
        max_length=20,
        choices=ACTIVITY_TYPE_CHOICES,
        default='Call',
        verbose_name="Activity Type"
    )
    subject = models.CharField(
        max_length=200,
        verbose_name="Subject / Title",
        help_text="e.g. Discussed pricing proposal, Intro call"
    )
    notes = models.TextField(
        verbose_name="Interaction Notes",
        help_text="Detailed notes about the call, meeting, or email conversation."
    )
    date = models.DateTimeField(
        default=timezone.now,
        verbose_name="Interaction Date & Time"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='activities',
        verbose_name="Logged By"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Logged At")

    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = "Activity"
        verbose_name_plural = "Activities"

    def __str__(self):
        return f"{self.get_activity_type_display()} with {self.customer.name} - {self.subject}"

    @property
    def icon_class(self):
        """Bootstrap Icon class corresponding to the interaction type."""
        icons = {
            'Call': 'bi-telephone-fill text-primary',
            'Meeting': 'bi-calendar-event-fill text-warning',
            'Email': 'bi-envelope-fill text-info',
            'Note': 'bi-journal-text text-success',
        }
        return icons.get(self.activity_type, 'bi-chat-dots-fill text-secondary')

    @property
    def badge_class(self):
        """Bootstrap badge styling."""
        badges = {
            'Call': 'bg-primary-subtle text-primary border border-primary-subtle',
            'Meeting': 'bg-warning-subtle text-warning-emphasis border border-warning-subtle',
            'Email': 'bg-info-subtle text-info-emphasis border border-info-subtle',
            'Note': 'bg-success-subtle text-success-emphasis border border-success-subtle',
        }
        return badges.get(self.activity_type, 'bg-light text-dark')
