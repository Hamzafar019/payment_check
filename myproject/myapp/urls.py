from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.organization_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('create-student/', views.create_student, name='create_student'),
    path('student/', views.student, name='student'),
    path('organization/', views.organization, name='organization'),
    path('create-subscription/', views.create_subscription, name='create_subscription'),
    path('superuser/', views.superuser, name='superuser'),
    path('subscribe/', views.subscribe, name='subscribe'),
    # path('organization_payment/', views.organization_payment, name='organization_payment'),
    path('make-payment/<int:subscription_id>/<str:month>/', views.make_payment, name='make_payment'),
    path('make-studentpayment/<int:subscription_id>/<str:month>/', views.make_studentpayment, name='make_studentpayment'),

    path('organization-view-paymenthistory/', views.organization_view_paymenthistory, name='organization_view_paymenthistory'),
    path('student-view-paymenthistory/', views.student_view_paymenthistory, name='student_view_paymenthistory'),
    
]
