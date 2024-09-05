import os
import sys
import string
import random
import django

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# Initialize Django
django.setup()

from django.core.management.base import BaseCommand

from post.models import Post, Comment
from users.models import CustomUser

class Command(BaseCommand):
    help = "Populate test data"

    def handle(self, *args, **kwargs):
        RANDOM_STR = lambda n: ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))
        password = "asd123@#$"

        self.stdout.write(self.style.SUCCESS("USER"))
        user, created = CustomUser.objects.get_or_create(username='user1')
        if created: user.set_password(password); user.save()

        Post.objects.bulk_create(
            Post(
                author = user,
                title = f"post-{i}",
                description = f"decs-{i}"
            )
            for i in range(1,11)
        )
        self.stdout.write(self.style.SUCCESS("Created Posts Successfully"))
        

# class Command(BaseCommand):
#     help = "Populate test data"

#     def handle(self, *args, **kwargs):
#         RANDOM_STR = lambda n: ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))

#         # Agency.objects.all().delete()
#         # Lead.objects.all().delete()

#         #region USERS
#         self.stdout.write(self.style.SUCCESS("USERS"))
#         password = "asd123@#$"


#         adminuser ,created = User.objects.get_or_create(username="adminuser", role=Role.ADMIN)
#         if created: adminuser.set_password(password); adminuser.save()

#         CHIEF_MANAGER, created = User.objects.get_or_create(username="CHIEF_MANAGER", role=Role.CHIEF_MANAGER)
#         if created: CHIEF_MANAGER.set_password(password); CHIEF_MANAGER.save()

#         MANAGER, created = User.objects.get_or_create(username="MANAGER", role=Role.MANAGER)
#         if created: MANAGER.set_password(password); MANAGER.save()



#         SALES_1, created = User.objects.get_or_create(username="SALES_1", role=Role.SALES)
#         if created: SALES_1.set_password(password); SALES_1.save()

#         SALES_2, created = User.objects.get_or_create(username="SALES_2", role=Role.SALES)
#         if created: SALES_2.set_password(password); SALES_2.save()

#         SALES_3, created = User.objects.get_or_create(username="SALES_3", role=Role.SALES)
#         if created: SALES_3.set_password(password); SALES_3.save()

#         SALES_4, created = User.objects.get_or_create(username="SALES_4", role=Role.SALES)
#         if created: SALES_4.set_password(password); SALES_4.save()



#         TELESALES_1, created = User.objects.get_or_create(username="TELESALES_1", role=Role.TELESALES)
#         if created: TELESALES_1.set_password(password); TELESALES_1.save()

#         TELESALES_2, created = User.objects.get_or_create(username="TELESALES_2", role=Role.TELESALES)
#         if created: TELESALES_2.set_password(password); TELESALES_2.save()

#         TELESALES_3, created = User.objects.get_or_create(username="TELESALES_3", role=Role.TELESALES)
#         if created: TELESALES_3.set_password(password); TELESALES_3.save()

#         TELESALES_4, created = User.objects.get_or_create(username="TELESALES_4", role=Role.TELESALES)
#         if created: TELESALES_4.set_password(password); TELESALES_4.save()



#         DATA_ENTRY, created = User.objects.get_or_create(username="DATA_ENTRY", role=Role.DATA_ENTRY)
#         if created: DATA_ENTRY.set_password(password); DATA_ENTRY.save()

#         DATA_ANALYST, created = User.objects.get_or_create(username="DATA_ANALYST", role=Role.DATA_ANALYST)
#         if created: DATA_ANALYST.set_password(password); DATA_ANALYST.save()


#         #endregion

#         #region AGENCIES
#         self.stdout.write(self.style.SUCCESS("AGENCIES"))

#         A1 = Agency.objects.create(name="Agency-1")
#         A2 = Agency.objects.create(name="Agency-2")
#         A3 = Agency.objects.create(name="Agency-3")
#         A4 = Agency.objects.create(name="Agency-4")


#         #endregion

#         #region AGENCIES USERS
#         self.stdout.write(self.style.SUCCESS("AGENCIES USERS"))

#         A1.users.set(
#             [CHIEF_MANAGER, MANAGER, SALES_1, TELESALES_1]
#         )
#         A2.users.set(
#             [CHIEF_MANAGER, MANAGER, SALES_2, TELESALES_2]
#         )
#         A3.users.set(
#             [CHIEF_MANAGER, SALES_3, TELESALES_3]
#         )
#         A4.users.set(
#             [MANAGER, SALES_4, TELESALES_4]
#         )

#         #endregion

#         #region LEADS
#         self.stdout.write(self.style.SUCCESS("LEADS"))
#         lead_types = LeadType.objects.all()
#         business_types = BusinessType.objects.all()

#         # unassigned leads
#         Lead.objects.bulk_create([
#             Lead(
#                 name=f"Un-Lead-{i}", phone=f"+023-{i}",
#                 email=f"Un.Lead.{i}@example.com",
#                 code=RANDOM_STR(5),
#                 lead_type=lead_types.first(),
#                 business_type=business_types.first()
#             )
#             for i in range(1, 11)
#         ])


#         # Agency-1 leads
#         A1_leads = Lead.objects.bulk_create([
#             Lead(
#                 name=f"A1-Lead-{i}", phone=f"+0235-{i}",
#                 email=f"A1.Lead.{i}@example.com",
#                 code=RANDOM_STR(5)
#             )
#             for i in range(1, 11)
#         ])

#         # Agency-2 leads
#         A2_leads = Lead.objects.bulk_create([
#             Lead(
#                 name=f"A2-Lead-{i}", phone=f"+0236-{i}",
#                 email=f"A2.Lead.{i}@example.com",
#                 code=RANDOM_STR(5),
#                 lead_type=lead_types.first()
#             )
#             for i in range(1, 11)
#         ])

#         #endregion

#         #region AGENCIES LEADS
#         self.stdout.write(self.style.SUCCESS("AGENCIES LEADS"))
#         from datetime import datetime, timedelta



#         A1.leads.set(A1_leads)
#         LeadAgency.objects.filter(agency=A1).update(
#             sales=SALES_1, tele=TELESALES_1,
#         )

#         A2.leads.set(A2_leads)
#         LeadAgency.objects.filter(agency=A2).update(
#             sales=SALES_2, tele=TELESALES_2, created_at=datetime.now() - timedelta(days=30)
#         )

#         #endregion


#         self.stdout.write(self.style.SUCCESS("Successfully populated test data"))
