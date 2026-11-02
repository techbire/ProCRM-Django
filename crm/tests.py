from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from crm.models import Customer, Lead, Activity


class CRMTests(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123',
            first_name='Test',
            last_name='User'
        )
        self.client = Client()

        # Create test customer
        self.customer = Customer.objects.create(
            name="Acme Corp Client",
            email="client@acmewidgets.com",
            phone="+1 555-1010",
            company="Acme Corp",
            address="123 Industrial Way"
        )

        # Create test lead
        self.lead = Lead.objects.create(
            name="Jane Prospective",
            email="jane@prospect.com",
            phone="+1 555-2020",
            source="Website",
            status="New",
            notes="Interested in enterprise tier."
        )

        # Create test activity
        self.activity = Activity.objects.create(
            customer=self.customer,
            lead=self.lead,
            activity_type="Call",
            subject="Intro call",
            notes="Discussed quarterly roadmap",
            created_by=self.user
        )

    def test_login_required_protection(self):
        """Unauthenticated requests must be redirected to login page."""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

        response = self.client.get(reverse('customer_list'))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('lead_list'))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('activity_list'))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_authenticated(self):
        """Authenticated user can view dashboard statistics."""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "CRM Overview")
        self.assertContains(response, "Total Customers")
        self.assertEqual(response.context['total_customers'], 1)
        self.assertEqual(response.context['total_leads'], 1)

    def test_customer_crud(self):
        """Test Customer creation, viewing, updating, and deletion."""
        self.client.login(username='testuser', password='testpassword123')

        # List
        response = self.client.get(reverse('customer_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Acme Corp Client")

        # Create
        response = self.client.post(reverse('customer_create'), {
            'name': 'New Customer Ltd',
            'email': 'new@customer.com',
            'phone': '123-456',
            'company': 'New Ltd',
            'address': 'Main street 1'
        })
        self.assertEqual(response.status_code, 302)
        new_customer = Customer.objects.get(email='new@customer.com')
        self.assertEqual(new_customer.name, 'New Customer Ltd')

        # Detail
        response = self.client.get(reverse('customer_detail', args=[new_customer.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New Customer Ltd')

        # Update
        response = self.client.post(reverse('customer_update', args=[new_customer.pk]), {
            'name': 'Updated Customer Name',
            'email': 'new@customer.com',
            'phone': '123-456',
            'company': 'Updated Ltd',
            'address': 'Main street 2'
        })
        self.assertEqual(response.status_code, 302)
        new_customer.refresh_from_db()
        self.assertEqual(new_customer.name, 'Updated Customer Name')

        # Delete
        response = self.client.post(reverse('customer_delete', args=[new_customer.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Customer.objects.filter(pk=new_customer.pk).exists())

    def test_lead_crud_and_conversion(self):
        """Test Lead management and one-click lead conversion to Customer."""
        self.client.login(username='testuser', password='testpassword123')

        # List
        response = self.client.get(reverse('lead_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Jane Prospective")

        # Convert Lead
        response = self.client.post(reverse('lead_convert', args=[self.lead.pk]))
        self.assertEqual(response.status_code, 302)
        self.lead.refresh_from_db()
        self.assertEqual(self.lead.status, 'Converted')
        self.assertIsNotNone(self.lead.customer)
        self.assertEqual(self.lead.customer.email, self.lead.email)

    def test_activity_logging(self):
        """Test logging interactions."""
        self.client.login(username='testuser', password='testpassword123')

        response = self.client.post(reverse('activity_create'), {
            'customer': self.customer.pk,
            'activity_type': 'Meeting',
            'subject': 'Boardroom Presentation',
            'notes': 'Presented Q3 deliverables',
            'date': '2026-11-02T14:30'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Activity.objects.filter(subject='Boardroom Presentation').exists())

    def test_customer_search(self):
        """Test searching customer list."""
        self.client.login(username='testuser', password='testpassword123')

        response = self.client.get(reverse('customer_list') + '?q=Acme')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Acme Corp Client")

        response = self.client.get(reverse('customer_list') + '?q=NonExistentQueryXYZ')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No customers matching "NonExistentQueryXYZ"')
