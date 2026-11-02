from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random

from crm.models import Customer, Lead, Activity


class Command(BaseCommand):
    help = "Populate the database with demo users, 25 customers, 25 leads, and 30 interaction activities."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Starting database seeding process..."))

        # 1. Create or get Admin Superuser
        admin_user, created = User.objects.get_or_create(username="admin")
        if created:
            admin_user.set_password("admin123")
            admin_user.email = "admin@example.com"
            admin_user.first_name = "Admin"
            admin_user.last_name = "Manager"
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Created superuser: admin / admin123"))
        else:
            self.stdout.write(self.style.WARNING("Superuser 'admin' already exists."))

        # 2. Seed 25 Customers
        customers_data = [
            {
                "name": "Sarah Connor",
                "email": "sarah.connor@cyberdyne.io",
                "phone": "+1 (555) 234-5678",
                "company": "Cyberdyne Systems",
                "address": "742 Evergreen Terrace, Los Angeles, CA 90001",
            },
            {
                "name": "Michael Scott",
                "email": "mscott@dundermifflin.com",
                "phone": "+1 (555) 345-6789",
                "company": "Dunder Mifflin Paper Co.",
                "address": "1725 Slough Avenue, Scranton, PA 18504",
            },
            {
                "name": "Bruce Wayne",
                "email": "bruce@wayneenterprises.com",
                "phone": "+1 (555) 456-7890",
                "company": "Wayne Enterprises",
                "address": "1007 Mountain Drive, Gotham City, NJ 07001",
            },
            {
                "name": "Tony Stark",
                "email": "tony@starkindustries.com",
                "phone": "+1 (555) 567-8901",
                "company": "Stark Industries",
                "address": "10880 Malibu Point, Malibu, CA 90265",
            },
            {
                "name": "Elena Rostova",
                "email": "elena.rostova@auroraglobal.de",
                "phone": "+49 30 901820",
                "company": "Aurora Global Logistics",
                "address": "Friedrichstraße 44, 10117 Berlin, Germany",
            },
            {
                "name": "David Kim",
                "email": "david.kim@nexastech.com",
                "phone": "+1 (555) 678-9012",
                "company": "Nexas Technologies",
                "address": "450 Mission St, San Francisco, CA 94105",
            },
            {
                "name": "Amara Okafor",
                "email": "amara.okafor@africarising.org",
                "phone": "+234 803 123 4567",
                "company": "Africa Rising Ventures",
                "address": "12 Marina Road, Victoria Island, Lagos, Nigeria",
            },
            {
                "name": "Liam O'Connor",
                "email": "liam.oconnor@clovercloud.ie",
                "phone": "+353 1 496 0000",
                "company": "Clover Cloud Computing",
                "address": "Grand Canal Dock, Dublin 2, Ireland",
            },
            {
                "name": "Sophia Martinez",
                "email": "sophia.m@solarisgreen.es",
                "phone": "+34 91 123 4567",
                "company": "Solaris Green Energy",
                "address": "Paseo de la Castellana 89, 28046 Madrid, Spain",
            },
            {
                "name": "Kenji Sato",
                "email": "kenji.sato@miraicorp.jp",
                "phone": "+81 3 5555 0143",
                "company": "Mirai Robotics Corp",
                "address": "6-10-1 Roppongi, Minato-ku, Tokyo 106-6108, Japan",
            },
            {
                "name": "Rachel Green",
                "email": "rachel@ralphlaurenpr.com",
                "phone": "+1 (555) 789-0123",
                "company": "Bloomingdale & Co",
                "address": "59th Street & Lexington Ave, New York, NY 10022",
            },
            {
                "name": "Alexander Wright",
                "email": "a.wright@wrightcapital.co.uk",
                "phone": "+44 20 7946 0912",
                "company": "Wright Asset Capital",
                "address": "25 Bank Street, Canary Wharf, London E14 5JP, UK",
            },
            {
                "name": "Priya Sharma",
                "email": "priya.sharma@zenithfin.in",
                "phone": "+91 22 2653 4000",
                "company": "Zenith Financial Services",
                "address": "Bandra Kurla Complex, Mumbai, Maharashtra 400051",
            },
            {
                "name": "Lucas Silva",
                "email": "lucas.silva@biomassa.br",
                "phone": "+55 11 3095 2000",
                "company": "Biomassa Renovaveis",
                "address": "Av. Paulista 1374, Sao Paulo, SP 01310-100, Brazil",
            },
            {
                "name": "Hannah Schmidt",
                "email": "hannah@bavarianauto.de",
                "phone": "+49 89 3820",
                "company": "Bavarian Automotive Parts",
                "address": "Petuelring 130, 80788 Munich, Germany",
            },
            {
                "name": "Marcus Vance",
                "email": "marcus.vance@vancemedia.com",
                "phone": "+1 (555) 890-1234",
                "company": "Vance Media Group",
                "address": "350 5th Ave, Empire State Bldg, New York, NY 10118",
            },
            {
                "name": "Chloe Dupont",
                "email": "chloe.dupont@atelierluxe.fr",
                "phone": "+33 1 42 68 55 00",
                "company": "Atelier Luxe Paris",
                "address": "15 Place Vendôme, 75001 Paris, France",
            },
            {
                "name": "Arjun Patel",
                "email": "arjun.patel@novushealth.com",
                "phone": "+1 (555) 901-2345",
                "company": "Novus Healthcare",
                "address": "200 Health Way, Boston, MA 02115",
            },
            {
                "name": "Grace Hopper",
                "email": "grace.hopper@compilertech.org",
                "phone": "+1 (555) 012-3456",
                "company": "Compiler Computing Labs",
                "address": "1 Broadway, Cambridge, MA 02142",
            },
            {
                "name": "Oliver Hansen",
                "email": "oliver@nordicdesign.dk",
                "phone": "+45 33 12 34 56",
                "company": "Nordic Design Studio",
                "address": "Bredgade 68, 1260 Copenhagen, Denmark",
            },
            {
                "name": "Zoe Kravitz",
                "email": "zoe.k@cinemagicprod.com",
                "phone": "+1 (555) 123-7890",
                "company": "Cinemagic Productions",
                "address": "500 S Buena Vista St, Burbank, CA 91521",
            },
            {
                "name": "Nathan Drake",
                "email": "nathan@unchartedexplorations.com",
                "phone": "+1 (555) 234-8901",
                "company": "Uncharted Maritime Logistics",
                "address": "Pier 39, The Embarcadero, San Francisco, CA 94133",
            },
            {
                "name": "Fatima Al-Mansoor",
                "email": "fatima@gulfheritage.ae",
                "phone": "+971 4 362 7000",
                "company": "Gulf Heritage Holdings",
                "address": "DIFC Gate Precinct 4, Dubai, UAE",
            },
            {
                "name": "Benjamin Franklin",
                "email": "ben@libertypress.org",
                "phone": "+1 (555) 345-9012",
                "company": "Liberty Printing House",
                "address": "320 Market Street, Philadelphia, PA 19106",
            },
            {
                "name": "Ingrid Bergman",
                "email": "ingrid.b@stockholmtelecom.se",
                "phone": "+46 8 500 0000",
                "company": "Stockholm Telecom AB",
                "address": "Stureplan 4, 114 35 Stockholm, Sweden",
            },
        ]

        created_customers = []
        for cdata in customers_data:
            customer, _ = Customer.objects.get_or_create(
                email=cdata["email"],
                defaults=cdata
            )
            created_customers.append(customer)

        self.stdout.write(self.style.SUCCESS(f"Seeded {len(created_customers)} customers."))

        # 3. Seed 25 Leads
        leads_data = [
            {
                "name": "Jordan Peterson",
                "email": "jordan.p@torontomaps.ca",
                "phone": "+1 (416) 555-0199",
                "source": "Website",
                "status": "New",
                "notes": "Requested a product demo through the marketing landing page form.",
                "customer": None,
            },
            {
                "name": "Jessica Pearson",
                "email": "jessica@pearsonhardman.com",
                "phone": "+1 (212) 555-0178",
                "source": "Referral",
                "status": "Interested",
                "notes": "Looking for enterprise CRM deployment for 120 legal associates. Budget approved.",
                "customer": None,
            },
            {
                "name": "Harvey Specter",
                "email": "harvey@pearsonhardman.com",
                "phone": "+1 (212) 555-0182",
                "source": "Referral",
                "status": "Contacted",
                "notes": "Followed up on contract negotiations. Needs SLA commitments by end of week.",
                "customer": None,
            },
            {
                "name": "Sarah Connor",
                "email": "sarah.connor@cyberdyne.io",
                "phone": "+1 (555) 234-5678",
                "source": "Website",
                "status": "Converted",
                "notes": "Successfully signed enterprise contract. Converted to active customer.",
                "customer": created_customers[0],
            },
            {
                "name": "Michael Scott",
                "email": "mscott@dundermifflin.com",
                "phone": "+1 (555) 345-6789",
                "source": "Cold Call",
                "status": "Converted",
                "notes": "Purchased annual license after product presentation in Scranton.",
                "customer": created_customers[1],
            },
            {
                "name": "Gita Gopinath",
                "email": "gita.g@globalpolicy.org",
                "phone": "+1 (202) 555-0134",
                "source": "Event",
                "status": "Interested",
                "notes": "Met at World Economic Forum. Discussed data privacy and team collaboration tools.",
                "customer": None,
            },
            {
                "name": "Carlos Gomez",
                "email": "carlos.g@bogotatech.co",
                "phone": "+57 1 555 4321",
                "source": "Social Media",
                "status": "New",
                "notes": "Inquired via LinkedIn campaign about monthly recurring subscription tiers.",
                "customer": None,
            },
            {
                "name": "Bruce Wayne",
                "email": "bruce@wayneenterprises.com",
                "phone": "+1 (555) 456-7890",
                "source": "Referral",
                "status": "Converted",
                "notes": "Direct executive referral. Converted to premier customer account.",
                "customer": created_customers[2],
            },
            {
                "name": "Diana Prince",
                "email": "diana.prince@antiquities.org",
                "phone": "+1 (202) 555-0191",
                "source": "Website",
                "status": "Contacted",
                "notes": "Sent introductory capabilities deck. Awaiting response on scheduling call.",
                "customer": None,
            },
            {
                "name": "Peter Parker",
                "email": "peter.parker@dailybugle.net",
                "phone": "+1 (212) 555-0144",
                "source": "Social Media",
                "status": "Lost",
                "notes": "Project cancelled due to budget constraints at media outlet.",
                "customer": None,
            },
            {
                "name": "Tony Stark",
                "email": "tony@starkindustries.com",
                "phone": "+1 (555) 567-8901",
                "source": "Event",
                "status": "Converted",
                "notes": "Converted lead. Exploring AI automation integration with CRM.",
                "customer": created_customers[3],
            },
            {
                "name": "Mei Lin",
                "email": "mei.lin@shanghaifab.cn",
                "phone": "+86 21 5555 6789",
                "source": "Website",
                "status": "Interested",
                "notes": "Evaluating CRM for supply chain team of 40 users. Wants localization in Mandarin.",
                "customer": None,
            },
            {
                "name": "Alexander Wright",
                "email": "a.wright@wrightcapital.co.uk",
                "phone": "+44 20 7946 0912",
                "source": "Referral",
                "status": "Converted",
                "notes": "Onboarded as premier European corporate client.",
                "customer": created_customers[11],
            },
            {
                "name": "Rachel Zane",
                "email": "rachel.zane@lawcorp.com",
                "phone": "+1 (212) 555-0165",
                "source": "Cold Call",
                "status": "Contacted",
                "notes": "Spoke regarding compliance archiving feature set. Meeting set for next Tuesday.",
                "customer": None,
            },
            {
                "name": "Siddharth Verma",
                "email": "sid.verma@bangaloreai.in",
                "phone": "+91 80 5555 1234",
                "source": "Email Campaign",
                "status": "New",
                "notes": "Clicked link in Spring Product Update email campaign.",
                "customer": None,
            },
            {
                "name": "Victoria Stone",
                "email": "vstone@sydneymining.com.au",
                "phone": "+61 2 5550 4321",
                "source": "Website",
                "status": "Interested",
                "notes": "Interested in mobile field access and offline sync features.",
                "customer": None,
            },
            {
                "name": "Lars Lindqvist",
                "email": "lars@helsinkidesign.fi",
                "phone": "+358 9 555 8765",
                "source": "Other",
                "status": "Lost",
                "notes": "Selected another legacy provider due to pre-existing ERP integration.",
                "customer": None,
            },
            {
                "name": "Elena Rostova",
                "email": "elena.rostova@auroraglobal.de",
                "phone": "+49 30 901820",
                "source": "Website",
                "status": "Converted",
                "notes": "Converted enterprise lead. European logistics deployment.",
                "customer": created_customers[4],
            },
            {
                "name": "Walter White",
                "email": "walter.white@abqchemicals.com",
                "phone": "+1 (505) 555-0187",
                "source": "Cold Call",
                "status": "Contacted",
                "notes": "Discussed bulk chemical inventory management integration.",
                "customer": None,
            },
            {
                "name": "Priya Sharma",
                "email": "priya.sharma@zenithfin.in",
                "phone": "+91 22 2653 4000",
                "source": "Referral",
                "status": "Converted",
                "notes": "Converted to client. Setup complete with custom permissions.",
                "customer": created_customers[12],
            },
            {
                "name": "Klaus Weber",
                "email": "klaus.weber@frankfurtfin.de",
                "phone": "+49 69 5555 9988",
                "source": "Event",
                "status": "New",
                "notes": "Handed business card during FinTech Europe Expo 2026.",
                "customer": None,
            },
            {
                "name": "Hannah Schmidt",
                "email": "hannah@bavarianauto.de",
                "phone": "+49 89 3820",
                "source": "Website",
                "status": "Converted",
                "notes": "Converted account. Deployed across 3 regional sales offices.",
                "customer": created_customers[14],
            },
            {
                "name": "Arthur Pendelton",
                "email": "arthur@camelotconsulting.co.uk",
                "phone": "+44 1632 960123",
                "source": "Email Campaign",
                "status": "Lost",
                "notes": "Client opted out. Internal restructuring put all software purchases on hold.",
                "customer": None,
            },
            {
                "name": "Nadia Morozova",
                "email": "nadia.m@praguemedia.cz",
                "phone": "+420 255 501 234",
                "source": "Social Media",
                "status": "Interested",
                "notes": "Requested a custom quote for 15 CRM team member accounts.",
                "customer": None,
            },
            {
                "name": "Oliver Hansen",
                "email": "oliver@nordicdesign.dk",
                "phone": "+45 33 12 34 56",
                "source": "Website",
                "status": "Converted",
                "notes": "Converted customer. Clean Scandinavian architectural agency setup.",
                "customer": created_customers[19],
            },
        ]

        created_leads = []
        for ldata in leads_data:
            lead, _ = Lead.objects.get_or_create(
                email=ldata["email"],
                defaults=ldata
            )
            created_leads.append(lead)

        self.stdout.write(self.style.SUCCESS(f"Seeded {len(created_leads)} leads."))

        # 4. Seed 30 Activities
        activity_templates = [
            ("Call", "Initial introductory telephone consultation", "Called client to introduce ProCRM, assess their team size, and review their software expectations. Client responded very positively."),
            ("Meeting", "Executive demonstration of CRM pipeline", "Presented live product walkthrough focusing on pipeline stages, customer profiles, and activity notes tracking."),
            ("Email", "Sent pricing proposal and implementation timeline", "Emailed customized tier pricing sheet and standard terms of service. Offered a 14-day assisted setup period."),
            ("Call", "Contract clarification and security review", "Phone discussion with head of IT concerning data encryption, role permissions, and local SQLite data isolation."),
            ("Meeting", "Weekly sales strategy check-in", "Met with account executives to align on quarterly revenue targets and pipeline deal velocity."),
            ("Note", "Customer requested invoice adjustment", "Client asked for annual invoicing upfront with tax identification code included on bill."),
            ("Email", "Follow-up email on feature roadmap", "Replied with details regarding upcoming export capabilities and custom reporting widgets."),
            ("Call", "Quarterly customer success check-in call", "Checked in on user adoption across teams. Overall satisfaction rating is 9.5/10."),
            ("Meeting", "Onboarding kickoff meeting", "Walked the leadership team through lead status transitions, customer data hygiene, and interaction logging best practices."),
            ("Note", "Lead converted successfully to full account", "Customer profile created, primary contact designated, and introductory welcome package sent."),
        ]

        now = timezone.now()
        activities_count = 0

        # Loop through customers and generate realistic interaction records
        for i, customer in enumerate(created_customers):
            # 1 to 2 activities per customer
            num_acts = 1 if i % 2 == 0 else 2
            for j in range(num_acts):
                template = activity_templates[(i + j) % len(activity_templates)]
                act_date = now - timedelta(days=random.randint(1, 30), hours=random.randint(1, 12))
                
                # Check if there is an associated lead for this customer
                linked_lead = customer.leads.first()

                Activity.objects.get_or_create(
                    customer=customer,
                    subject=f"{template[1]} - {customer.name}",
                    defaults={
                        "lead": linked_lead,
                        "activity_type": template[0],
                        "notes": template[2],
                        "date": act_date,
                        "created_by": admin_user,
                    }
                )
                activities_count += 1
                if activities_count >= 30:
                    break
            if activities_count >= 30:
                break

        self.stdout.write(self.style.SUCCESS(f"Seeded {activities_count} customer interaction activities."))
        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))

