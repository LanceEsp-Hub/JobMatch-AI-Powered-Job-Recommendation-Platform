from django.db import models
from django.contrib.auth.models import User



# Resume Model
class Resume(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    resume_file = models.FileField(upload_to='resumes/')
    
    # Define status choices for Resume
    STATUS_CHOICES = [
        ('successful', 'Successful'),
        ('unsuccessful', 'Unsuccessful'),
        ('pending', 'Pending'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)  # Status field for the resume

    def __str__(self):
        return self.name

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    skills_required = models.TextField()

    def __str__(self):
        return self.title

from django.db import models
from django.contrib.auth.models import User

# JobMatch Model
class JobMatch(models.Model):
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)  # Match score
    
    # The status for the job match itself
    STATUS_CHOICES = [
        ('successful', 'Successful'),
        ('unsuccessful', 'Unsuccessful'),
        ('pending', 'Pending'),
    ]
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'  # Default to 'pending' if not set
    )
    
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.job.title} matched with {self.user.username} ({self.get_status_display()})'


