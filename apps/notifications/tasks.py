from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_welcome_email(user_email, username):
    """Send welcome email asynchronously"""
    subject = 'Welcome to SafeYouth AI!'
    message = f'Hi {username},\n\nWelcome to SafeYouth AI! We are here to support you.\n\nBest regards,\nSafeYouth AI Team'
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )
    return f'Welcome email sent to {user_email}'

@shared_task
def process_analytics_data():
    """Process analytics in background"""
    # Your analytics processing logic here
    print("Processing analytics data...")
    return "Analytics processed"

@shared_task
def send_daily_reminders():
    """Send daily mood tracking reminders"""
    # Logic to send reminders to users
    print("Sending daily reminders...")
    return "Reminders sent"
