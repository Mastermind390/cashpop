from django.db import models
from django.contrib.auth.models import User
import uuid

CATEGORY_CHOICES = [
        ('social_media', 'social_media'),
        ('videos', 'videos'),
        ('surveys', 'survey'),
        ('others', 'others'),
    ]




class Task(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='others')
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField(max_length=500, default="")
    estimated_time_mins = models.PositiveIntegerField(default=0)
    reward = models.PositiveIntegerField(default=0)
    amount_tasker = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    task_earning = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    locked_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    referral_code = models.CharField(max_length=10, unique=True, blank=True)
    referred_by = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    date_joined = models.DateTimeField(auto_now_add=True)
    streak = models.PositiveIntegerField(default=0)
    total_task_completed = models.PositiveIntegerField(default=0)
    total_reward = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = str(uuid.uuid4().hex[:10])  # Generate unique referral code
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class UserTask(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    proof_image = models.ImageField(upload_to='images/', default="images/hero-illustration.svg")  # Optional proof (screenshot)
    proof_username = models.CharField(max_length=200, default="user.firstname")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task.title



class UserLogin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'login_date')


class UserAccountDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=10)
    full_name = models.CharField(max_length=200)

    def __str__(self):
        return self.full_name
    


class Withdrawal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveBigIntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name}, {self.amount}"
