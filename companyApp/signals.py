from django.db.models.signals import post_save
from django.dispatch import receiver
from authenticationApp.models import User
from .models import CompanyDetailsTable, Resource_Code_L1_Table


@receiver(post_save, sender=CompanyDetailsTable)
def create_resource_codes(sender, instance, created, **kwargs):
    print("saving 5 resourse level 1 ...")
    if created:  # Check if a new CompanyDetailsTable row is created
        default_codes = [
            "MATERIALS",
            "Labor",
            "EQUIPMENT",
            "Subcontractors",
            "OTHERS"
        ]
        # Create a Resource_Code_L1_Table entry for each default code
        for code in default_codes:
            Resource_Code_L1_Table.objects.create(
                Company_Details=instance,
                Resource_Code_L1=code
            )