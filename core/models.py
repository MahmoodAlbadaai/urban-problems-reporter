from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

# Model for different types of urban issues
class IssueType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    icon = models.ImageField(upload_to='issue_icons/', null=True, blank=True)
    
    def __str__(self):
        return self.name

# Model for locations in the city
class Location(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    address = models.TextField()
    
    def __str__(self):
        return self.name

# Model for reported issues
class Issue(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    ]
    
    # Foreign key to IssueType
    issue_type = models.ForeignKey(IssueType, on_delete=models.CASCADE, related_name='issues')
    
    # Foreign key to Location
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='issues')
    
    title = models.CharField(max_length=100)
    description = models.TextField()
    
    # Reporter information
    reporter_name = models.CharField(max_length=100)
    reporter_email = models.EmailField()
    reporter_phone = models.CharField(max_length=20, blank=True, null=True)
    
    # Issue details
    reported_date = models.DateTimeField(default=timezone.now)
    incident_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Issue images
    image = models.ImageField(upload_to='issue_images/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"

# Model for resolution of issues
class Resolution(models.Model):
    # Foreign key to Issue
    issue = models.OneToOneField(Issue, on_delete=models.CASCADE, related_name='resolution')
    
    # Foreign key to User (authority member who resolved it)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    resolution_date = models.DateTimeField(default=timezone.now)
    resolution_details = models.TextField()
    
    # Before and after images
    before_image = models.ImageField(upload_to='resolution_images/before/', blank=True, null=True)
    after_image = models.ImageField(upload_to='resolution_images/after/', blank=True, null=True)
    
    # Was this featured as a success story?
    featured = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Resolution for {self.issue.title}"

# Model for comments on issues
class Comment(models.Model):
    # Foreign key to Issue
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    
    # Optional foreign key to User (for authority comments)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # For non-user comments
    author_name = models.CharField(max_length=100, blank=True, null=True)
    author_email = models.EmailField(blank=True, null=True)
    
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.user:
            return f"Comment by {self.user.username} on {self.issue.title}"
        return f"Comment by {self.author_name} on {self.issue.title}"
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_authority = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Profile for {self.user.username}"
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)