from django.db import models
from django.utils import timezone
from accounts.models import CustomUser
from coursedb.models import Course

class Company(models.Model):
    LOCATION_CHOICES = [
        ('chennai', 'Chennai'),
        ('bangalore', 'Bangalore'),
        ('hyderabad', 'Hyderabad'),
        ('others', 'Others'),
    ]
    PORTAL_CHOICES = [
        ('naukri', 'Naukri'),
        ('linkedin', 'LinkedIn'),
        ('glassdoor', 'Glassdoor'),
        ('indeed', 'Indeed'),
        ('placement_india', 'Placement India'),
        ('freshersworld', 'Freshersworld'),
        ('shine', 'Shine'),
        ('many_jobs', 'Many Jobs'),
        ('internshala', 'Internshala'),
        ('quickr_jobs', 'Quickr Jobs'),
        ('google_jobs', 'Google Jobs'),
        ('monster', 'Monster'),
        ('company_website', 'Company Website'),
        ('others', 'Others')
    ]
    PROGRESS_CHOICES = [
        ('resume_shared', 'Resume Shared'),
        ('interview_scheduling', 'Interview Scheduling'),
        ('interview_not_conducted','Interview Not Conducted'),
        ('interview_completed', 'Interview Completed'),
    ]
    company_code = models.CharField(max_length=20, unique=True, editable=False)
    date = models.DateField(default=timezone.now)
    portal = models.CharField(max_length=100, choices=PORTAL_CHOICES)
    other_portal = models.CharField(max_length=255, blank=True, null=True)
    company_name = models.CharField(max_length=255)
    spoc = models.CharField(max_length=255)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    location = models.CharField(max_length=255, choices=LOCATION_CHOICES)
    other_location = models.CharField(max_length=255, blank=True, null=True)
    progress = models.CharField(max_length=50, choices=PROGRESS_CHOICES, default='resume_shared')
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company_name} ({self.company_code})"

    def save(self, *args, **kwargs):
        if not self.company_code:
            last_company = Company.objects.all().order_by('id').last()
            if not last_company:
                self.company_code = 'COMP0001'
            else:
                last_code = last_company.company_code
                last_number = int(last_code.replace('COMP', ''))
                new_number = last_number + 1
                self.company_code = f'COMP{new_number:04d}'
        super().save(*args, **kwargs)
class Interview(models.Model):
    ROUND_CHOICES = [
        ('aptitude', 'Aptitude'),
        ('gd',"Group Discussion"),
        ('technical', 'Technical'),
        ('hr', 'HR'),
        ('task', 'Task Work'),
    ]
    VENUE_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
    ]
    LOCATION_CHOICES = [
        ('chennai', 'Chennai'),
        ('bangalore', 'Bangalore'),
        ('hyderabad', 'Hyderabad'),
        ('others', 'Others'),
    ]
    venue = models.CharField(
        max_length=20,
        choices=VENUE_CHOICES,
        default='offline'
    )

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='scheduled_interviews')
    applying_role = models.CharField(max_length=255)
    courses = models.ManyToManyField(Course)
    interview_round = models.CharField(max_length=50, choices=ROUND_CHOICES)
    round_number = models.PositiveIntegerField(default=1)
    parent_interview = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_rounds')
    location = models.CharField(max_length=255, choices=LOCATION_CHOICES)
    other_location = models.CharField(max_length=255, blank=True, null=True)
    interview_date = models.DateField()
    interview_time = models.TimeField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Interview for {self.applying_role} at {self.company.company_name} on {self.interview_date}"
from studentsdb.models import Student

class InterviewStudent(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('not_attended','Not Attended'),
        ('selected', 'Selected'),
        ('rejected', 'Rejected'),
        ('placed', 'Placed'),
    ]
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name='student_status')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='interview_statuses')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    reason = models.TextField(blank=True, null=True)
    offer_letter = models.FileField(upload_to='offer_letters/', blank=True, null=True)

    def __str__(self):
        return f"{self.student} - {self.interview}"
