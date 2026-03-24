"""
AEGISAI - accounts/models.py
Database models matching the project documentation schema.
"""

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# ─────────────────────────────────────────────────────────────────────────────
# DJANGO ADMIN USER  (kept for Django admin panel / superuser only)
# ─────────────────────────────────────────────────────────────────────────────

# CustomUser and UserRegister removed. Using standard Django User.

from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_suspended = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        # Failsafe if profile doesn't exist for older users
        UserProfile.objects.get_or_create(user=instance)


# ─────────────────────────────────────────────────────────────────────────────
# TABLE 2: POLICE_REGISTER
# ─────────────────────────────────────────────────────────────────────────────

class PoliceRegister(models.Model):
    police_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)          # stores hashed password
    badge_number = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)

    is_active = models.BooleanField(default=True)
    status = models.CharField(
        max_length=10,
        choices=[('active','Active'), ('suspended','Suspended')],
        default='active'
    )

    class Meta:
        db_table = 'POLICE_REGISTER'

    def __str__(self):
        return f"{self.firstname} {self.lastname} – Badge: {self.badge_number}"

    def get_full_name(self):
        return f"{self.firstname} {self.lastname}"

    @property
    def is_authenticated(self):
        return True

    @property
    def role(self):
        return 'POLICE'


# ─────────────────────────────────────────────────────────────────────────────
# TABLE 3: CYBER_CRIME_REPORT
# ─────────────────────────────────────────────────────────────────────────────

class CyberCrimeReport(models.Model):
    TYPE_CHOICES = [
        ('PHISHING', 'Phishing'),
        ('MALWARE', 'Malware'),
        ('IDENTITY_THEFT', 'Identity Theft'),
        ('FRAUD', 'Online Fraud'),
        ('HARASSMENT', 'Cyber Harassment'),
        ('DATA_BREACH', 'Data Breach'),
        ('DDOS', 'DDoS Attack'),
        ('OTHER', 'Other'),
    ]

    report_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, default='Untitled Report')
    crime_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField()
    date_reported = models.DateTimeField(auto_now_add=True)

    # Optional links to who submitted / who handles
    submitted_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='reports'
    )
    assigned_police = models.ForeignKey(
        PoliceRegister, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='assigned_reports'
    )
    status = models.CharField(
        max_length=15,
        choices=[
            ('PENDING', 'Pending'),
            ('REVIEWING', 'Under Review'),
            ('RESOLVED', 'Resolved'),
            ('DISMISSED', 'Dismissed'),
        ],
        default='PENDING',
    )
    evidence_details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'CYBER_CRIME_REPORT'
        ordering = ['-created_at']

    def __str__(self):
        return f"Report #{self.report_id} – {self.title}"


# ─────────────────────────────────────────────────────────────────────────────
# TABLE 4: FILEDATA
# ─────────────────────────────────────────────────────────────────────────────

class FileData(models.Model):
    file_id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True)

    # Extra detail for the file-share module
    file = models.FileField(upload_to='shared_files/%Y/%m/%d/', blank=True, null=True)
    sender = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='sent_files'
    )
    receiver = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='received_files'
    )
    message = models.TextField(blank=True)
    scan_result = models.CharField(
        max_length=10,
        choices=[
            ('CLEAN', 'Clean'),
            ('MALICIOUS', 'Malicious'),
            ('PENDING', 'Pending'),
            ('ERROR', 'Scan Error'),
        ],
        default='PENDING',
    )
    scan_details = models.TextField(blank=True)

    class Meta:
        db_table = 'FILEDATA'
        ordering = ['-upload_date']

    def __str__(self):
        return self.file_name

    def file_extension(self):
        import os
        return os.path.splitext(self.file_name)[1].lower()


# ─────────────────────────────────────────────────────────────────────────────
# TABLE 5: ATTACK
# ─────────────────────────────────────────────────────────────────────────────

class Attack(models.Model):
    attack_id = models.AutoField(primary_key=True)
    attack_type = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    rank = models.IntegerField(default=0)
    file_id = models.ForeignKey(
        FileData, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='attacks',
        db_column='file_id'
    )

    class Meta:
        db_table = 'ATTACK'
        ordering = ['-date']

    def __str__(self):
        return f"{self.attack_type} (rank {self.rank})"


# ─────────────────────────────────────────────────────────────────────────────
# TABLE 6: DDOS_DATASET
# ─────────────────────────────────────────────────────────────────────────────

class DdosDataset(models.Model):
    id = models.AutoField(primary_key=True)
    ddos_data = models.TextField()
    attack_result = models.CharField(max_length=100)

    class Meta:
        db_table = 'DDOS_DATASET'

    def __str__(self):
        return f"DDoS record #{self.id} → {self.attack_result}"


# ─────────────────────────────────────────────────────────────────────────────
# TABLE 7: FEEDBACK
# ─────────────────────────────────────────────────────────────────────────────

class Feedback(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    email = models.EmailField()
    experience = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES, default=3)
    comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'FEEDBACK'

    def __str__(self):
        return f"Feedback from {self.name} – Rating {self.rating}"


# ─────────────────────────────────────────────────────────────────────────────
# TABLE 8: REQUEST_TO_ADMIN
# ─────────────────────────────────────────────────────────────────────────────

class RequestToAdmin(models.Model):
    id = models.AutoField(primary_key=True)
    ddos_data = models.TextField()
    attack_result = models.CharField(max_length=100)
    name = models.CharField(max_length=150)

    class Meta:
        db_table = 'REQUEST_TO_ADMIN'

    def __str__(self):
        return f"Request from {self.name} → {self.attack_result}"


# ─────────────────────────────────────────────────────────────────────────────
# THREAT LOG  (internal – linked to FILEDATA)
# ─────────────────────────────────────────────────────────────────────────────

class ThreatLog(models.Model):
    SEVERITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]

    file_data = models.ForeignKey(
        FileData, on_delete=models.CASCADE, related_name='threats'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='threat_logs'
    )
    filename = models.CharField(max_length=255)
    threat_type = models.CharField(max_length=100)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='HIGH')
    details = models.TextField()
    detected_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'THREAT_LOG'
        ordering = ['-detected_at']

    def __str__(self):
        return f"Threat: {self.filename} – {self.threat_type}"
