from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('accountant', 'Accountant'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.user.username

class Organization(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE , null=True)
    name = models.CharField(max_length=255)
    address = models.TextField() 
    contact_email = models.EmailField()

    def __str__(self):
        return self.name

class Subscription(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class OrganizationSubscription(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    date_of_subscription = models.DateField()

    def __str__(self):
        return f"{self.organization.name} - {self.subscription.name} ({self.date_of_subscription})"

class Student(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    enrollment_date = models.DateField()

    def __str__(self):
        return self.user_profile.user.username

class Payment(models.Model):
    organizationsubscription = models.ForeignKey(OrganizationSubscription, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    # organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.DateField()

    def __str__(self):
        return f'{self.student.user_profile.user.username} - {self.month.strftime("%Y-%m")}'

class Transaction(models.Model):
    organizationsubscription = models.ForeignKey(OrganizationSubscription, on_delete=models.CASCADE, null=True)
    # organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.DateField()

    def __str__(self):
        return f'{self.organizationsubscription.organization.name} - {self.month.strftime("%Y-%m")}'
