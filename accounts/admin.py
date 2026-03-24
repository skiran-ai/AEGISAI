"""
AEGISAI – accounts/admin.py
Django admin registrations for all new schema models.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    PoliceRegister,
    CyberCrimeReport, FileData, Attack,
    DdosDataset, Feedback, RequestToAdmin,
    ThreatLog,
)


# Custom User and User Register removed.


# ─────────────────────────────────────────────────────────────────────────────
# TABLE 2: POLICE_REGISTER
# ─────────────────────────────────────────────────────────────────────────────

@admin.register(PoliceRegister)
class PoliceRegisterAdmin(admin.ModelAdmin):
    list_display  = ('police_id', 'firstname', 'lastname', 'email', 'badge_number')
    search_fields = ('firstname', 'lastname', 'email', 'badge_number')
    ordering      = ('police_id',)


# ─────────────────────────────────────────────────────────────────────────────
# TABLE 3: CYBER_CRIME_REPORT
# ─────────────────────────────────────────────────────────────────────────────

@admin.register(CyberCrimeReport)
class CyberCrimeReportAdmin(admin.ModelAdmin):
    list_display  = ('report_id', 'crime_type', 'status', 'submitted_by', 'assigned_police', 'date_reported')
    list_filter   = ('crime_type', 'status', 'date_reported')
    search_fields = ('description',)
    ordering      = ('-date_reported',)


# ─────────────────────────────────────────────────────────────────────────────
# TABLE 4: FILEDATA
# ─────────────────────────────────────────────────────────────────────────────

@admin.register(FileData)
class FileDataAdmin(admin.ModelAdmin):
    list_display  = ('file_id', 'file_name', 'sender', 'receiver', 'scan_result', 'upload_date')
    list_filter   = ('scan_result', 'upload_date')
    search_fields = ('file_name',)
    ordering      = ('-upload_date',)


# ─────────────────────────────────────────────────────────────────────────────
# TABLE 5: ATTACK
# ─────────────────────────────────────────────────────────────────────────────

@admin.register(Attack)
class AttackAdmin(admin.ModelAdmin):
    list_display  = ('attack_id', 'attack_type', 'rank', 'file_id', 'date')
    list_filter   = ('attack_type', 'date')
    search_fields = ('attack_type',)
    ordering      = ('-date',)


# ─────────────────────────────────────────────────────────────────────────────
# TABLE 6: DDOS_DATASET
# ─────────────────────────────────────────────────────────────────────────────

@admin.register(DdosDataset)
class DdosDatasetAdmin(admin.ModelAdmin):
    list_display  = ('id', 'attack_result', 'ddos_data')
    search_fields = ('attack_result', 'ddos_data')


# ─────────────────────────────────────────────────────────────────────────────
# TABLE 7: FEEDBACK
# ─────────────────────────────────────────────────────────────────────────────

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display  = ('id', 'name', 'email', 'rating')
    list_filter   = ('rating',)
    search_fields = ('name', 'email', 'experience', 'comments')


# ─────────────────────────────────────────────────────────────────────────────
# TABLE 8: REQUEST_TO_ADMIN
# ─────────────────────────────────────────────────────────────────────────────

@admin.register(RequestToAdmin)
class RequestToAdminAdmin(admin.ModelAdmin):
    list_display  = ('id', 'name', 'attack_result', 'ddos_data')
    search_fields = ('name', 'attack_result')


# ─────────────────────────────────────────────────────────────────────────────
# THREAT LOG
# ─────────────────────────────────────────────────────────────────────────────

@admin.register(ThreatLog)
class ThreatLogAdmin(admin.ModelAdmin):
    list_display  = ('filename', 'user', 'threat_type', 'severity', 'detected_at')
    list_filter   = ('severity', 'threat_type', 'detected_at')
    search_fields = ('filename', 'details')
    ordering      = ('-detected_at',)
