from django.db import models
from django.utils import timezone

class User(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    email = models.EmailField()
    about = models.TextField()
    profile_image = models.ImageField(upload_to='profile_images/')
    resume = models.FileField(upload_to='resumes/', blank=True, help_text='Upload your resume in PDF format')
    github_username = models.CharField(max_length=100)
    github_url = models.URLField(blank=True)
    linkedin_username = models.CharField(max_length=100)
    linkedin_url = models.URLField(blank=True)
    
    def __str__(self):
        return self.name

class SkillCategory(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Skill Categories"

class Skill(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(SkillCategory, related_name='skills', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Technology(models.Model):
    name = models.CharField(max_length=50)
    
    class Meta:
        verbose_name_plural = 'Technologies'
    
    def __str__(self):
        return self.name

class Experience(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    period = models.CharField(max_length=100)
    description = models.TextField()
    technologies = models.ManyToManyField(Technology, related_name='experiences')
    
    def __str__(self):
        return f"{self.title} at {self.company}"

class Tag(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/')
    github_link = models.URLField(blank=True)
    live_link = models.URLField(blank=True)
    technologies = models.ManyToManyField(Technology)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.subject}"

class Certification(models.Model):
    title = models.CharField(max_length=200)
    provider = models.CharField(max_length=200)
    issue_date = models.DateField()
    image = models.ImageField(upload_to='certifications/')
    skills = models.CharField(max_length=500, help_text='Enter skills separated by commas')
    certificate_url = models.URLField(blank=True, null=True, help_text='URL to view the certificate')
    verify_url = models.URLField(blank=True, null=True, help_text='URL to verify the certificate')
    
    class Meta:
        ordering = ['-issue_date']  # Sort by date in descending order
        
    def __str__(self):
        return f"{self.title} - {self.provider}"
        
    def get_skills_list(self):
        return [skill.strip() for skill in self.skills.split(',')]