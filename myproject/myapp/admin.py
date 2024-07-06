from django.contrib import admin
from .models import UserProfile, Subscription, Organization, Student, Payment, Transaction, OrganizationSubscription

admin.site.register(UserProfile)
admin.site.register(Subscription)
admin.site.register(Organization)
admin.site.register(Student)
admin.site.register(Payment)
admin.site.register(Transaction)
admin.site.register(OrganizationSubscription)
