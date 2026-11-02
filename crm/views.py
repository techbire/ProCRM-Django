from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone

from .models import Customer, Lead, Activity
from .forms import (
    UserRegistrationForm,
    UserLoginForm,
    CustomerForm,
    LeadForm,
    ActivityForm
)


# ==============================================================================
# AUTHENTICATION VIEWS
# ==============================================================================

def register_view(request):
    """
    Handles user registration.
    Allows new users to create an account and immediately log in.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically log the user in after successful registration
            login(request, user)
            messages.success(request, f"Welcome to ProCRM, {user.first_name or user.username}! Your account has been created.")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegistrationForm()

    return render(request, 'crm/auth/register.html', {'form': form})


def login_view(request):
    """
    Handles user login.
    Validates credentials and starts a user session.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = UserLoginForm()

    return render(request, 'crm/auth/login.html', {'form': form})


def logout_view(request):
    """
    Logs out the current user and clears session data.
    """
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('login')


# ==============================================================================
# DASHBOARD VIEW
# ==============================================================================

@login_required
def dashboard_view(request):
    """
    Main CRM Dashboard.
    Displays summary statistics, conversion metrics, recent leads, customers, and activities.
    """
    total_customers = Customer.objects.count()
    total_leads = Lead.objects.count()
    active_leads = Lead.objects.filter(status__in=['New', 'Contacted', 'Interested']).count()
    converted_leads = Lead.objects.filter(status='Converted').count()
    lost_leads = Lead.objects.filter(status='Lost').count()

    # Calculate lead conversion rate
    if total_leads > 0:
        conversion_rate = round((converted_leads / total_leads) * 100, 1)
    else:
        conversion_rate = 0.0

    # Recent items
    recent_customers = Customer.objects.all()[:5]
    recent_leads = Lead.objects.select_related('customer')[:5]
    recent_activities = Activity.objects.select_related('customer', 'lead', 'created_by')[:5]

    context = {
        'total_customers': total_customers,
        'total_leads': total_leads,
        'active_leads': active_leads,
        'converted_leads': converted_leads,
        'lost_leads': lost_leads,
        'conversion_rate': conversion_rate,
        'recent_customers': recent_customers,
        'recent_leads': recent_leads,
        'recent_activities': recent_activities,
    }
    return render(request, 'crm/dashboard.html', context)


# ==============================================================================
# CUSTOMER MANAGEMENT (CRUD)
# ==============================================================================

@login_required
def customer_list(request):
    """
    List all customers with optional search by name, email, or company.
    """
    query = request.GET.get('q', '').strip()
    customers = Customer.objects.all()

    if query:
        customers = customers.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(company__icontains=query) |
            Q(phone__icontains=query)
        )

    context = {
        'customers': customers,
        'query': query,
        'total_count': customers.count(),
    }
    return render(request, 'crm/customers/customer_list.html', context)


@login_required
def customer_detail(request, pk):
    """
    Detailed profile view for a single customer.
    Displays customer contact information, related leads, and full interaction activity history.
    Also provides a quick form to log an activity directly on this page.
    """
    customer = get_object_or_404(Customer, pk=pk)
    customer_leads = customer.leads.all()
    customer_activities = customer.activities.select_related('created_by', 'lead').all()

    # Pre-filled activity form for convenience
    quick_activity_form = ActivityForm(initial={'customer': customer, 'date': timezone.now()})

    context = {
        'customer': customer,
        'customer_leads': customer_leads,
        'customer_activities': customer_activities,
        'quick_activity_form': quick_activity_form,
    }
    return render(request, 'crm/customers/customer_detail.html', context)


@login_required
def customer_create(request):
    """
    Add a new customer.
    """
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            messages.success(request, f"Customer '{customer.name}' was created successfully!")
            return redirect('customer_detail', pk=customer.pk)
        else:
            messages.error(request, "Please review the form errors below.")
    else:
        form = CustomerForm()

    return render(request, 'crm/customers/customer_form.html', {
        'form': form,
        'title': 'Add New Customer',
        'is_edit': False,
    })


@login_required
def customer_update(request, pk):
    """
    Edit an existing customer.
    """
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save()
            messages.success(request, f"Customer '{customer.name}' was updated successfully!")
            return redirect('customer_detail', pk=customer.pk)
        else:
            messages.error(request, "Please review the form errors below.")
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'crm/customers/customer_form.html', {
        'form': form,
        'customer': customer,
        'title': f'Edit Customer: {customer.name}',
        'is_edit': True,
    })


@login_required
def customer_delete(request, pk):
    """
    Delete a customer after confirmation.
    """
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'POST':
        customer_name = customer.name
        customer.delete()
        messages.success(request, f"Customer '{customer_name}' has been permanently deleted.")
        return redirect('customer_list')

    return render(request, 'crm/customers/customer_confirm_delete.html', {'customer': customer})


# ==============================================================================
# LEAD MANAGEMENT (CRUD)
# ==============================================================================

@login_required
def lead_list(request):
    """
    List all leads with search and status filtering (New, Contacted, Interested, Converted, Lost).
    """
    query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip()

    leads = Lead.objects.select_related('customer').all()

    if status_filter:
        leads = leads.filter(status=status_filter)

    if query:
        leads = leads.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query) |
            Q(source__icontains=query) |
            Q(notes__icontains=query)
        )

    # Lead count per status for filtering chips/tabs
    status_counts = {
        'all': Lead.objects.count(),
        'New': Lead.objects.filter(status='New').count(),
        'Contacted': Lead.objects.filter(status='Contacted').count(),
        'Interested': Lead.objects.filter(status='Interested').count(),
        'Converted': Lead.objects.filter(status='Converted').count(),
        'Lost': Lead.objects.filter(status='Lost').count(),
    }

    context = {
        'leads': leads,
        'query': query,
        'status_filter': status_filter,
        'status_counts': status_counts,
    }
    return render(request, 'crm/leads/lead_list.html', context)


@login_required
def lead_detail(request, pk):
    """
    View detailed information about a single lead and its interactions.
    """
    lead = get_object_or_404(Lead.objects.select_related('customer'), pk=pk)
    lead_activities = lead.activities.select_related('created_by', 'customer').all()

    context = {
        'lead': lead,
        'lead_activities': lead_activities,
    }
    return render(request, 'crm/leads/lead_detail.html', context)


@login_required
def lead_create(request):
    """
    Add a new sales lead.
    """
    # Allow pre-selecting customer if customer_id is provided in URL query string
    customer_id = request.GET.get('customer_id')
    initial_data = {}
    if customer_id:
        try:
            initial_data['customer'] = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            pass

    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save()
            messages.success(request, f"Lead '{lead.name}' created successfully!")
            return redirect('lead_detail', pk=lead.pk)
        else:
            messages.error(request, "Please review the form errors below.")
    else:
        form = LeadForm(initial=initial_data)

    return render(request, 'crm/leads/lead_form.html', {
        'form': form,
        'title': 'Add New Lead',
        'is_edit': False,
    })


@login_required
def lead_update(request, pk):
    """
    Edit an existing lead.
    """
    lead = get_object_or_404(Lead, pk=pk)

    if request.method == 'POST':
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            lead = form.save()
            messages.success(request, f"Lead '{lead.name}' updated successfully!")
            return redirect('lead_detail', pk=lead.pk)
        else:
            messages.error(request, "Please review the form errors below.")
    else:
        form = LeadForm(instance=lead)

    return render(request, 'crm/leads/lead_form.html', {
        'form': form,
        'lead': lead,
        'title': f'Edit Lead: {lead.name}',
        'is_edit': True,
    })


@login_required
def lead_delete(request, pk):
    """
    Delete a lead after confirmation.
    """
    lead = get_object_or_404(Lead, pk=pk)

    if request.method == 'POST':
        lead_name = lead.name
        lead.delete()
        messages.success(request, f"Lead '{lead_name}' has been deleted.")
        return redirect('lead_list')

    return render(request, 'crm/leads/lead_confirm_delete.html', {'lead': lead})


@login_required
def lead_convert(request, pk):
    """
    Convert a Lead into a Customer with one click:
    1. Checks if customer already exists (by email) or creates a new Customer.
    2. Links lead to customer and marks status as 'Converted'.
    3. Logs an activity record indicating the conversion.
    """
    lead = get_object_or_404(Lead, pk=pk)

    if request.method == 'POST':
        if not lead.customer:
            # Check if customer already exists with this email
            customer = Customer.objects.filter(email=lead.email).first()
            if not customer:
                customer = Customer.objects.create(
                    name=lead.name,
                    email=lead.email,
                    phone=lead.phone,
                    company="",
                    address=""
                )
            lead.customer = customer

        lead.status = 'Converted'
        lead.save()

        # Record activity
        Activity.objects.create(
            customer=lead.customer,
            lead=lead,
            activity_type='Note',
            subject='Lead Converted to Customer',
            notes=f"Lead was successfully converted into customer profile on {timezone.now().strftime('%Y-%m-%d %H:%M')}.",
            created_by=request.user
        )

        messages.success(request, f"Lead '{lead.name}' has been successfully converted to a Customer!")
        return redirect('customer_detail', pk=lead.customer.pk)

    return redirect('lead_detail', pk=lead.pk)


# ==============================================================================
# ACTIVITY MANAGEMENT
# ==============================================================================

@login_required
def activity_list(request):
    """
    View activity history across all customers and leads.
    Filterable by activity type (Call, Meeting, Email, Note) and searchable.
    """
    activity_type = request.GET.get('type', '').strip()
    query = request.GET.get('q', '').strip()

    activities = Activity.objects.select_related('customer', 'lead', 'created_by').all()

    if activity_type:
        activities = activities.filter(activity_type=activity_type)

    if query:
        activities = activities.filter(
            Q(subject__icontains=query) |
            Q(notes__icontains=query) |
            Q(customer__name__icontains=query) |
            Q(lead__name__icontains=query)
        )

    context = {
        'activities': activities,
        'activity_type': activity_type,
        'query': query,
        'total_count': activities.count(),
    }
    return render(request, 'crm/activities/activity_list.html', context)


@login_required
def activity_create(request):
    """
    Record a new interaction (Call, Meeting, Email, or Note).
    Allows pre-filling customer_id or lead_id via query parameters.
    """
    initial_data = {'date': timezone.now()}
    customer_id = request.GET.get('customer_id')
    lead_id = request.GET.get('lead_id')

    if customer_id:
        try:
            initial_data['customer'] = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            pass

    if lead_id:
        try:
            lead = Lead.objects.get(pk=lead_id)
            initial_data['lead'] = lead
            if not customer_id and lead.customer:
                initial_data['customer'] = lead.customer
        except Lead.DoesNotExist:
            pass

    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.created_by = request.user
            activity.save()
            messages.success(request, "Activity recorded successfully!")

            # If user submitted from customer detail page, return there
            return_to = request.POST.get('return_to')
            if return_to == 'customer' and activity.customer:
                return redirect('customer_detail', pk=activity.customer.pk)
            elif return_to == 'lead' and activity.lead:
                return redirect('lead_detail', pk=activity.lead.pk)

            return redirect('activity_list')
        else:
            messages.error(request, "Please review the form errors below.")
    else:
        form = ActivityForm(initial=initial_data)

    return render(request, 'crm/activities/activity_form.html', {
        'form': form,
        'title': 'Log New Interaction',
    })


@login_required
def activity_delete(request, pk):
    """
    Delete an activity entry.
    """
    activity = get_object_or_404(Activity, pk=pk)
    customer_id = activity.customer_id

    if request.method == 'POST':
        activity.delete()
        messages.success(request, "Activity removed successfully.")
        return redirect('customer_detail', pk=customer_id)

    return redirect('activity_list')
