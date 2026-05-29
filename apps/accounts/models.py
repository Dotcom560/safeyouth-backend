from django.db import models
from django.contrib.auth.models import User

class TeenProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teen_profile')
    nickname = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=100, blank=True)
    age_range = models.CharField(max_length=20, choices=[
        ('13-15', '13-15 years'),
        ('16-18', '16-18 years'),
        ('19-21', '19-21 years'),
    ], default='16-18')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'accounts'
    
    def __str__(self):
        return self.nickname

class MoodLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mood_logs')
    mood_score = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=3)
    mood_label = models.CharField(max_length=20, choices=[
        ('happy', '😊 Happy'),
        ('sad', '😢 Sad'),
        ('anxious', '😰 Anxious'),
        ('angry', '😤 Angry'),
        ('calm', '😌 Calm'),
    ])
    note = models.TextField(blank=True)
    triggers = models.CharField(max_length=200, blank=True)
    date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = 'accounts'
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.user.username} - {self.mood_label} on {self.date}"
