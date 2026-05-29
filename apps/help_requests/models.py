from django.db import models
from django.contrib.auth.models import User

class HelpRequest(models.Model):
    TYPE_CHOICES = [
        ('abuse', 'Abuse'),
        ('drug_pressure', 'Drug Pressure'),
        ('violence', 'Violence'),
        ('bullying', 'Bullying'),
        ('mental_health', 'Mental Health'),
        ('pregnancy', 'Pregnancy Help'),
        ('other', 'Other'),
    ]
    
    URGENCY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('emergency', 'Emergency'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewing', 'Reviewing'),
        ('assigned', 'Assigned'),
        ('resolved', 'Resolved'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='help_requests')
    request_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField()
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES, default='medium')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    is_anonymous = models.BooleanField(default=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_requests')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'help_requests'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_request_type_display()} - {self.user.username} ({self.status})"
