from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_verified = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    adhar_card = models.ImageField(upload_to='documents/adhar/', blank=True, null=True)
    pan_card = models.ImageField(upload_to='documents/pan/', blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

# models.py
from django.db import models
from django.conf import settings  # to link to CustomUser
from django.utils import timezone

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=255, blank=True)
    body = models.TextField()
    attachment = models.FileField(upload_to='message_attachments/', blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender} to {self.receiver} - {self.subject or 'No Subject'}"

from django.db import models

from django.db import models

class LandRecord(models.Model):
    LAND_TYPE_CHOICES = [
        ('agriculture', 'Agriculture'),
        ('residential', 'Residential'),
        ('industrial', 'Industrial'),
        ('commercial', 'Commercial'),
        ('other', 'Other'),
    ]

    place = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    land_type = models.CharField(max_length=50, choices=LAND_TYPE_CHOICES)

    def __str__(self):
        return f"{self.place} - {self.land_type}"

class LandImage(models.Model):
    land_record = models.ForeignKey(
        LandRecord, related_name='images', on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='land_images/')

    def __str__(self):
        return f"Image for {self.land_record.place}"

class LandProperty(models.Model):
    sellers = models.ManyToManyField('SellerProfile')
    
    place = models.ForeignKey(
        'LandRecord', 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='properties_by_place'
    )
    land_record = models.ForeignKey(
        LandRecord, 
        on_delete=models.CASCADE,
        related_name='properties_by_record',
        blank=True, null=True
    )
    
    location = models.CharField(max_length=255)
    map_url = models.URLField(blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    is_ekhata_registered = models.BooleanField(default=False)
    land_use_type = models.CharField(
        max_length=50,
        choices=[
            ('agriculture', 'Agriculture'),
            ('residential', 'Residential'),
            ('other', 'Other'),
        ]
    )
    expected_price = models.PositiveIntegerField()
    description = models.TextField()
    is_sold = models.BooleanField(default=False)
    registration_number = models.CharField(max_length=100, blank=True, null=True)
    last_tax_paid_receipt = models.FileField(upload_to='tax_receipts/', blank=True, null=True)

    def __str__(self):
        return f"{self.place} - {self.location}"

class BuyerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    preferred_area = models.ForeignKey(LandRecord, on_delete=models.SET_NULL, null=True)
    budget_min = models.PositiveIntegerField()
    budget_max = models.PositiveIntegerField()

class SellerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    verified_by_admin = models.BooleanField(default=False)

class LegalCase(models.Model):
    land = models.ForeignKey(LandProperty, on_delete=models.CASCADE)
    case_number = models.CharField(max_length=50)
    document = models.FileField(upload_to='documents/cases/')
    remarks = models.TextField(blank=True)

class OwnershipHistory(models.Model):
    land = models.ForeignKey(LandProperty, on_delete=models.CASCADE)
    owner_name = models.CharField(max_length=100)
    ownership_order = models.PositiveIntegerField()
    new_owner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
