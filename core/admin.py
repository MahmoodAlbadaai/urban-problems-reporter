from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import IssueType, Location, Issue, Resolution, Comment

class IssueTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    search_fields = ('name', 'address')

class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'issue_type', 'location', 'status', 'reported_date')
    list_filter = ('status', 'issue_type', 'reported_date')
    search_fields = ('title', 'description', 'reporter_name', 'reporter_email')
    date_hierarchy = 'reported_date'

class ResolutionAdmin(admin.ModelAdmin):
    list_display = ('issue', 'resolution_date', 'resolved_by', 'featured')
    list_filter = ('featured', 'resolution_date')
    search_fields = ('resolution_details',)
    date_hierarchy = 'resolution_date'

class CommentAdmin(admin.ModelAdmin):
    list_display = ('issue', 'author_name', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('comment_text', 'author_name', 'author_email')
    date_hierarchy = 'created_at'

# Register the models with their custom admin classes
admin.site.register(IssueType, IssueTypeAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Resolution, ResolutionAdmin)
admin.site.register(Comment, CommentAdmin)