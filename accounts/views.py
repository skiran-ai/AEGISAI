"""
AEGISAI – accounts/views.py
Session-based auth for USER and POLICE; Django auth for ADMIN.
All models match the new schema tables.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as dj_login, logout as dj_logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.http import FileResponse
from django.contrib.auth.models import User
from .forms import (
    UserRegisterForm, PoliceRegistrationForm,
    UserLoginForm, PoliceLoginForm, AdminLoginForm,
    UpdateProfileForm, ChangePasswordForm,
    FeedbackForm, CyberCrimeReportForm, FileShareForm,
)
from .models import (
    PoliceRegister,
    CyberCrimeReport, FileData, ThreatLog,
    Feedback, DdosDataset, RequestToAdmin,
)
from .decorators import user_required, admin_required, police_required
from scanner import scan_file


# ─────────────────────────────────────────────────────────────────────────────
# SESSION HELPERS
# ─────────────────────────────────────────────────────────────────────────────

SESSION_USER_ID   = 'auth_user_id'
SESSION_USER_ROLE = 'auth_user_role'


def _session_login(request, obj, role):
    """Store user info in session (for USER / POLICE)."""
    if role == 'USER':
        # Default User model uses 'id', which is also 'pk'
        request.session[SESSION_USER_ID] = obj.pk
    else:
        request.session[SESSION_USER_ID] = obj.police_id
    request.session[SESSION_USER_ROLE] = role


def _session_logout(request):
    request.session.pop(SESSION_USER_ID, None)
    request.session.pop(SESSION_USER_ROLE, None)


def get_session_user(request):
    """
    Returns (user_obj, role) for USER/POLICE sessions,
    or (request.user, 'ADMIN') for Django-auth admins.
    """
    role = request.session.get(SESSION_USER_ROLE)
    uid  = request.session.get(SESSION_USER_ID)

    if role == 'USER' and uid:
        try:
            return User.objects.get(pk=uid), 'USER'
        except User.DoesNotExist:
            pass

    if role == 'POLICE' and uid:
        try:
            return PoliceRegister.objects.get(pk=uid), 'POLICE'
        except PoliceRegister.DoesNotExist:
            pass

    # Fall back to Django auth (ADMIN)
    if request.user.is_authenticated and request.user.is_superuser:
        return request.user, 'ADMIN'

    return None, None


def _is_logged_in(request):
    user, role = get_session_user(request)
    return user is not None


def _redirect_by_role(request):
    _, role = get_session_user(request)
    if role == 'ADMIN':
        return redirect('admin_dashboard')
    if role == 'POLICE':
        return redirect('police_dashboard')
    if role == 'USER':
        return redirect('user_dashboard')
    return redirect('home')


# ─────────────────────────────────────────────────────────────────────────────
# HOME
# ─────────────────────────────────────────────────────────────────────────────

def home(request):
    if _is_logged_in(request):
        return _redirect_by_role(request)
    return render(request, 'accounts/home.html')


# ─────────────────────────────────────────────────────────────────────────────
# USER AUTH
# ─────────────────────────────────────────────────────────────────────────────

def user_register(request):
    if _is_logged_in(request):
        return _redirect_by_role(request)
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            _session_login(request, user, 'USER')
            messages.success(request, 'Registration successful. Welcome to AEGISAI!')
            return redirect('user_dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    if _is_logged_in(request):
        return _redirect_by_role(request)
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user_obj']
            if hasattr(user, 'profile') and user.profile.is_suspended:
                messages.error(request, 'Your account has been suspended')
                return render(request, 'accounts/login.html', {'form': form})
            _session_login(request, user, 'USER')
            return redirect('user_dashboard')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


@user_required
def user_dashboard(request):
    user, _ = get_session_user(request)
    report_count    = CyberCrimeReport.objects.filter(submitted_by=user).count()
    files_sent      = FileData.objects.filter(sender=user).count()
    files_received  = FileData.objects.filter(receiver=user, scan_result='CLEAN').count()
    threats_found   = ThreatLog.objects.filter(user=user).count()
    feedback_count  = Feedback.objects.count()
    context = {
        'active_page': 'home',
        'current_user': user,
        'report_count': report_count,
        'files_sent': files_sent,
        'files_received': files_received,
        'threats_found': threats_found,
        'feedback_count': feedback_count,
    }
    return render(request, 'accounts/user_dashboard.html', context)


# ─────────────────────────────────────────────────────────────────────────────
# UPDATE PROFILE
# ─────────────────────────────────────────────────────────────────────────────

@user_required
def update_profile(request):
    user, _ = get_session_user(request)
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('update_profile')
    else:
        form = UpdateProfileForm(instance=user)

    password_form = ChangePasswordForm(user)
    context = {
        'form': form,
        'password_form': password_form,
        'active_page': 'profile',
        'current_user': user,
    }
    return render(request, 'accounts/update_profile.html', context)


@user_required
def change_password(request):
    user, _ = get_session_user(request)
    if request.method == 'POST':
        form = ChangePasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password changed successfully.')
            return redirect('update_profile')
        else:
            profile_form = UpdateProfileForm(instance=user)
            context = {
                'form': profile_form,
                'password_form': form,
                'active_page': 'profile',
                'current_user': user,
            }
            return render(request, 'accounts/update_profile.html', context)
    return redirect('update_profile')


# ─────────────────────────────────────────────────────────────────────────────
# FILE SHARE
# ─────────────────────────────────────────────────────────────────────────────

@user_required
def file_share(request):
    user, _ = get_session_user(request)
    if request.method == 'POST':
        form = FileShareForm(request.POST, request.FILES, current_user=user)
        if form.is_valid():
            receiver = form.cleaned_data['receiver']
            if receiver.pk == user.pk:
                messages.error(request, 'You cannot send a file to yourself.')
                return redirect('file_share')

            shared = form.save(commit=False)
            shared.sender = user
            shared.receiver = receiver
            shared.file_name = request.FILES['file'].name
            shared.save()

            # ── AI malware scan ──
            result = scan_file(shared.file.path, shared.file_name)
            if result['is_malicious']:
                shared.scan_result  = 'MALICIOUS'
                shared.scan_details = result['details']
                shared.save()
                ThreatLog.objects.create(
                    file_data=shared,
                    user=user,
                    filename=shared.file_name,
                    threat_type=result['threat_type'],
                    severity=result['severity'],
                    details=result['details'],
                )
                messages.warning(
                    request,
                    f'File "{shared.file_name}" was flagged as MALICIOUS by the AI scanner. '
                    f'A threat log has been created.'
                )
            else:
                shared.scan_result  = 'CLEAN'
                shared.scan_details = result['details']
                shared.save()
                messages.success(
                    request,
                    f'File "{shared.file_name}" scanned clean and sent to {receiver.get_full_name()}.'
                )
            return redirect('file_share')
    else:
        form = FileShareForm(current_user=user)

    sent_files = FileData.objects.filter(sender=user)
    users = User.objects.filter(is_superuser=False, is_staff=False).exclude(id=user.id)
    
    context = {
        'form': form,
        'users': users,
        'sent_files': sent_files,
        'active_page': 'fileshare',
        'current_user': user,
    }
    return render(request, 'accounts/file_share.html', context)


# ─────────────────────────────────────────────────────────────────────────────
# FILE INBOX
# ─────────────────────────────────────────────────────────────────────────────

@user_required
def file_inbox(request):
    user, _ = get_session_user(request)
    received_files = FileData.objects.filter(receiver=user).order_by('-upload_date')
    context = {
        'received_files': received_files,
        'active_page': 'fileinbox',
        'current_user': user,
    }
    return render(request, 'accounts/file_inbox.html', context)


@user_required
def download_file(request, pk):
    user, _ = get_session_user(request)
    shared = get_object_or_404(FileData, pk=pk)
    if shared.sender != user and shared.receiver != user:
        messages.error(request, 'Access denied.')
        return redirect('file_inbox')
    if shared.scan_result == 'MALICIOUS' and shared.receiver == user:
        messages.error(request, 'This file was flagged as malicious and cannot be downloaded.')
        return redirect('file_inbox')
    return FileResponse(
        open(shared.file.path, 'rb'),
        as_attachment=True,
        filename=shared.file_name,
    )


# ─────────────────────────────────────────────────────────────────────────────
# MY FEEDBACK
# ─────────────────────────────────────────────────────────────────────────────

@user_required
def my_feedback(request):
    user, _ = get_session_user(request)
    if request.method == 'POST':
        subject = request.POST.get("subject", "No Subject")
        category = request.POST.get("category", "general")
        message = request.POST.get("message", "")

        # Map to the existing model fields to adhere to the rule of not changing models.
        Feedback.objects.create(
            name=subject,
            email=getattr(user, 'email', ''),
            experience=message,
            comments=category,
            rating=1 if category == 'bug' else (5 if category == 'feature' else 3)
        )
        
        messages.success(request, 'Feedback submitted successfully.')
        return redirect('my_feedback')

    feedbacks = Feedback.objects.filter(email=getattr(user, 'email', '')).order_by('-id')
    context = {
        'feedbacks': feedbacks,
        'active_page': 'feedback',
        'current_user': user,
    }
    return render(request, 'accounts/my_feedback.html', context)


@user_required
def delete_feedback(request, pk):
    user, _ = get_session_user(request)
    feedback = get_object_or_404(Feedback, pk=pk, email=user.email)
    feedback.delete()
    messages.success(request, 'Feedback deleted.')
    return redirect('my_feedback')


# ─────────────────────────────────────────────────────────────────────────────
# USER REPORTS  (CYBER_CRIME_REPORT)
# ─────────────────────────────────────────────────────────────────────────────

@user_required
def user_reports(request):
    user, _ = get_session_user(request)
    if request.method == 'POST':
        form = CyberCrimeReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.submitted_by = user
            report.save()
            messages.success(request, 'Report submitted successfully.')
            return redirect('user_reports')
    else:
        form = CyberCrimeReportForm()

    reports = CyberCrimeReport.objects.filter(submitted_by=user)
    context = {
        'form': form,
        'reports': reports,
        'active_page': 'reports',
        'current_user': user,
    }
    return render(request, 'accounts/user_reports.html', context)


@user_required
def report_detail(request, pk):
    user, _ = get_session_user(request)
    report = get_object_or_404(CyberCrimeReport, pk=pk, submitted_by=user)
    context = {
        'report': report,
        'active_page': 'reports',
        'current_user': user,
    }
    return render(request, 'accounts/report_detail.html', context)


# ─────────────────────────────────────────────────────────────────────────────
# ADMIN AUTH
# ─────────────────────────────────────────────────────────────────────────────

def admin_login(request):
    if _is_logged_in(request):
        return _redirect_by_role(request)
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            admin_user = form.cleaned_data['user_obj']
            dj_login(request, admin_user, backend='accounts.backends.EmailBackend')
            request.session[SESSION_USER_ROLE] = 'ADMIN'
            return redirect('admin_dashboard')
    else:
        form = AdminLoginForm()
    return render(request, 'accounts/admin_login.html', {'form': form})


@admin_required
def admin_dashboard(request):
    total_users   = User.objects.count()
    total_police  = PoliceRegister.objects.count()
    active_threats = ThreatLog.objects.count()
    total_reports  = CyberCrimeReport.objects.count()
    context = {
        'total_users': total_users,
        'total_police': total_police,
        'active_threats': active_threats,
        'total_reports': total_reports,
        'active_page': 'dashboard',
    }
    return render(request, 'accounts/admin_dashboard.html', context)


@admin_required
def admin_users(request):
    users = User.objects.all().order_by('id')
    # Handle approve/reject actions (if needed for User model, though standard User doesn't have status)
    return render(request, 'accounts/admin_users.html', {'users': users, 'active_page': 'users'})


@admin_required
def admin_police(request):
    if request.method == "POST":
        police_id = request.POST.get("police_id")
        action = request.POST.get("action")
        if police_id and action:
            police = get_object_or_404(PoliceRegister, pk=police_id)
            if action == "suspend":
                police.status = 'suspended'
                police.is_active = False
                police.save()
                messages.success(request, f"Officer {police.get_full_name()} suspended.")
            elif action == "activate":
                police.status = 'active'
                police.is_active = True
                police.save()
                messages.success(request, f"Officer {police.get_full_name()} activated.")
            elif action == "dismiss":
                officer_name = police.get_full_name()
                police.delete()
                messages.success(request, f"Officer {officer_name} dismissed.")
            return redirect('admin_police')

    police_officers = PoliceRegister.objects.all().order_by('police_id')
    return render(request, 'accounts/admin_police.html', {
        'police_officers': police_officers,
        'active_page': 'police',
    })


@admin_required
def admin_incidents(request):
    if request.method == "POST":
        report_id = request.POST.get("report_id")
        police_id = request.POST.get("assigned_police")
        
        if report_id:
            report = get_object_or_404(CyberCrimeReport, pk=report_id)
            if police_id:
                police = get_object_or_404(PoliceRegister, pk=police_id)
                report.assigned_police = police
                messages.success(request, f'Case assigned to {police.get_full_name()} successfully.')
            else:
                report.assigned_police = None
                messages.success(request, 'Case assignment cleared.')
            report.save()
            return redirect('admin_incidents')

    incidents = CyberCrimeReport.objects.all().order_by('-date_reported')
    police_users = PoliceRegister.objects.filter(status='active').order_by('firstname')
    return render(request, 'accounts/admin_incidents.html', {
        'incidents': incidents,
        'police_users': police_users,
        'active_page': 'incidents',
    })


@admin_required
def admin_incident_detail(request, pk):
    incident = get_object_or_404(CyberCrimeReport, pk=pk)
    police_officers = PoliceRegister.objects.all()

    if request.method == 'POST':
        police_id = request.POST.get('assigned_police')
        if police_id:
            officer = get_object_or_404(PoliceRegister, pk=police_id)
            incident.assigned_police = officer
            incident.save()
            messages.success(request, f'Case assigned to {officer.get_full_name()} successfully.')
        else:
            incident.assigned_police = None
            incident.save()
            messages.success(request, 'Case assignment cleared.')
        return redirect('admin_incident_detail', pk=pk)

    return render(request, 'accounts/admin_incident_detail.html', {
        'incident': incident,
        'police_officers': police_officers,
        'active_page': 'incidents',
    })


@admin_required
def admin_feedback(request):
    feedbacks = Feedback.objects.all().order_by('-id')
    return render(request, 'accounts/admin_feedback.html', {
        'feedbacks': feedbacks,
        'active_page': 'feedback',
    })


@admin_required
def admin_threats(request):
    threat_logs = ThreatLog.objects.all().order_by('-detected_at')
    return render(request, 'accounts/admin_threats.html', {
        'threat_logs': threat_logs,
        'active_page': 'requests',
    })

@admin_required
def toggle_suspend_user(request, user_id):
    if request.method == 'POST':
        from .models import UserProfile
        user_to_toggle = get_object_or_404(User, pk=user_id)
        profile, _ = UserProfile.objects.get_or_create(user=user_to_toggle)
        profile.is_suspended = not profile.is_suspended
        profile.save()
        status_text = "suspended" if profile.is_suspended else "activated"
        messages.success(request, f"User {user_to_toggle.get_full_name()} successfully {status_text}.")
    return redirect('admin_threats')


# ─────────────────────────────────────────────────────────────────────────────
# POLICE AUTH
# ─────────────────────────────────────────────────────────────────────────────

def police_register(request):
    if _is_logged_in(request):
        return _redirect_by_role(request)
    if request.method == 'POST':
        form = PoliceRegistrationForm(request.POST)
        if form.is_valid():
            officer = form.save()
            _session_login(request, officer, 'POLICE')
            messages.success(request, 'Police registration successful.')
            return redirect('police_dashboard')
    else:
        form = PoliceRegistrationForm()
    return render(request, 'accounts/police_register.html', {'form': form})


def police_login(request):
    if _is_logged_in(request):
        return _redirect_by_role(request)
    if request.method == 'POST':
        form = PoliceLoginForm(request.POST)
        if form.is_valid():
            officer = form.cleaned_data['user_obj']
            if getattr(officer, 'status', 'active') == 'suspended':
                messages.error(request, "Account suspended")
                return render(request, 'accounts/police_login.html', {'form': form})
            _session_login(request, officer, 'POLICE')
            return redirect('police_dashboard')
    else:
        form = PoliceLoginForm()
    return render(request, 'accounts/police_login.html', {'form': form})


@police_required
def police_dashboard(request):
    user, _ = get_session_user(request)
    assigned_count    = CyberCrimeReport.objects.filter(assigned_police=user).count()
    active_investigations = CyberCrimeReport.objects.filter(status='REVIEWING').count()
    resolved_cases    = CyberCrimeReport.objects.filter(status='RESOLVED').count()
    pending_reports   = CyberCrimeReport.objects.filter(status='PENDING').count()
    recent_threat_logs = ThreatLog.objects.all().order_by('-detected_at')[:5]
    context = {
        'assigned_count': assigned_count,
        'active_investigations': active_investigations,
        'resolved_cases': resolved_cases,
        'pending_reports': pending_reports,
        'recent_threat_logs': recent_threat_logs,
        'active_page': 'dashboard',
        'current_user': user,
    }
    return render(request, 'accounts/police_dashboard.html', context)


@police_required
def police_reports(request):
    reports = CyberCrimeReport.objects.all().order_by('-date_reported')
    return render(request, 'accounts/police_reports.html', {
        'reports': reports,
        'active_page': 'reports',
    })


@police_required
def police_report_detail(request, pk):
    report = get_object_or_404(CyberCrimeReport, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        valid_statuses = dict(report._meta.get_field('status').choices)
        if new_status in valid_statuses:
            report.status = new_status
            report.save()
            messages.success(request, 'Report status updated successfully.')
            return redirect('police_report_detail', pk=pk)
    return render(request, 'accounts/police_report_detail.html', {
        'report': report,
        'active_page': 'reports',
    })


@police_required
def police_threats(request):
    threat_logs = ThreatLog.objects.all().order_by('-detected_at')
    return render(request, 'accounts/police_threats.html', {
        'threat_logs': threat_logs,
        'active_page': 'threats',
    })


# ─────────────────────────────────────────────────────────────────────────────
# LOGOUT
# ─────────────────────────────────────────────────────────────────────────────

def user_logout(request):
    _session_logout(request)
    if request.user.is_authenticated:
        dj_logout(request)          # also clear Django session for admin
    messages.success(request, 'You have been logged out.')
    return redirect('home')
