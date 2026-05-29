from django.contrib import admin
from apps.accounts.models import TeenProfile, MoodLog

@admin.register(TeenProfile)
class TeenProfileAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'user', 'age_range', 'location', 'created_at']
    search_fields = ['nickname', 'user__username']
    list_filter = ['age_range', 'created_at']

@admin.register(MoodLog)
class MoodLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'mood_label', 'mood_score', 'date']
    list_filter = ['mood_label', 'date']
    search_fields = ['user__username', 'note']
