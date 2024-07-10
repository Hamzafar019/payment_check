from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Organization, Student, Subscription, OrganizationSubscription, Transaction, Payment
from .forms import SubscriptionForm 
from .forms import OrganizationSignupForm, StudentCreationForm, OrganizationSubscriptionForm
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from .models import Organization, UserProfile




def organizationtransaction_check_required(view_func):
    def wrapper(request, *args, **kwargs):
        user_profile = request.user
        organization = get_object_or_404(Organization, user=user_profile)

        organization_subscriptions = OrganizationSubscription.objects.filter(organization=organization)
        print("SHIT\n\n\n\n\n")
        total_students = Student.objects.filter(organization=organization).count()

        for subscription in organization_subscriptions:
            start_date = subscription.date_of_subscription
            end_date = date.today()
            current_date = start_date
            
            amount = subscription.subscription.price
            total_amount=amount*total_students
            while current_date <= end_date:
                month_str = current_date.strftime("%Y-%m-%d")
                end_month=end_date.strftime("%Y-%m-%d")
                end_object= datetime.strptime(end_month, '%Y-%m-%d').date()
                date_obj = datetime.strptime(month_str, '%Y-%m-%d').date()
                transaction_count = Transaction.objects.filter(
                    organizationsubscription=subscription,
                    month__month=date_obj.month,
                ).count()
                if(end_object.month!=date_obj.month and date_obj.day<end_object.day ):
                    
                    if transaction_count == 0:
                        redirect_url= reverse('organization_view_paymenthistory') + '?alert=clear_dues'
                        
                        return redirect(redirect_url)
                    
                    transaction = Transaction.objects.filter(
                        organizationsubscription=subscription,
                        month__month=date_obj.month,
                    ).first()
                    if(transaction_count!=0):
                        # print(transaction.amount,transaction.id)
                        payment=transaction.amount
                        total_amount_float = float(total_amount)
                        if(payment<(.75*total_amount_float)):
                            redirect_url= reverse('login') + '?alert=less_payment'
                            
                            return redirect(redirect_url)

                current_date += relativedelta(months=1)
                
        # If no condition is met, continue with the original view function
        return view_func(request, *args, **kwargs)

    return wrapper





def studentorganizationtransaction_check_required(view_func):
    def wrapper(request, *args, **kwargs):
        user = request.user
        user_profile = get_object_or_404(UserProfile, user=user)
        student = get_object_or_404(Student, user_profile=user_profile)
        organization = student.organization
        organization_subscriptions = OrganizationSubscription.objects.filter(organization=organization)
        total_students = Student.objects.filter(organization=organization).count()

        for subscription in organization_subscriptions:
            start_date = subscription.date_of_subscription
            end_date = date.today()
            current_date = start_date
            
            amount = subscription.subscription.price
            total_amount=amount*total_students
            while current_date <= end_date:
                month_str = current_date.strftime("%Y-%m-%d")
                date_obj = datetime.strptime(month_str, '%Y-%m-%d').date()
                
                end_month=end_date.strftime("%Y-%m-%d")
                end_object= datetime.strptime(end_month, '%Y-%m-%d').date()
                transaction_count = Transaction.objects.filter(
                    organizationsubscription=subscription,
                    month__month=date_obj.month,
                ).count()
                if(end_object.month!=date_obj.month and date_obj.day<end_object.day ):

                    if transaction_count == 0:
                        # Redirect to student_view_paymenthistory if more than 1 payment exists
                        redirect_url= reverse('login') + '?alert=organization_clear_dues'
                        
                        return redirect(redirect_url)
                    
                    transaction = Transaction.objects.filter(
                        organizationsubscription=subscription,
                        month__month=date_obj.month,
                    ).first()
                    if(transaction_count!=0):
                        # print(transaction.amount,transaction.id)
                        # print("\n\n\n\najeeb")
                        payment=transaction.amount
                        total_amount_float = float(total_amount)
                        if(payment<(.75*total_amount_float)):
                            redirect_url= reverse('login') + '?alert=less_payment'
                            
                            return redirect(redirect_url)

                current_date += relativedelta(months=1)
                
        # If no condition is met, continue with the original view function
        return view_func(request, *args, **kwargs)

    return wrapper







def payment_check_required(view_func):
    def wrapper(request, *args, **kwargs):
        user = request.user
        user_profile = get_object_or_404(UserProfile, user=user)
        student = get_object_or_404(Student, user_profile=user_profile)
        organization = student.organization
        organization_subscriptions = OrganizationSubscription.objects.filter(organization=organization)
        total_students = Student.objects.filter(organization=organization).count()

        for subscription in organization_subscriptions:
            start_date = subscription.date_of_subscription
            end_date = date.today()
            current_date = start_date
            
            while current_date <= end_date:
                month_str = current_date.strftime("%Y-%m-%d")
                date_obj = datetime.strptime(month_str, '%Y-%m-%d').date()
                
                end_month=end_date.strftime("%Y-%m-%d")
                end_object= datetime.strptime(end_month, '%Y-%m-%d').date()
                transaction_count = Payment.objects.filter(
                    student=student,
                    organizationsubscription=subscription,
                    month__month=date_obj.month,
                ).count()
                # print("FFFF\n\n\n")
                # print(transaction_count)
                if(end_object.month!=date_obj.month and date_obj.day<end_object.day ):

                    if transaction_count == 0:

                        # Redirect to student_view_paymenthistory if more than 1 payment exists
                        redirect_url= reverse('student_view_paymenthistory') + '?alert=clear_dues'
                        
                        return redirect(redirect_url)

                current_date += relativedelta(months=1)
                
        # If no condition is met, continue with the original view function
        return view_func(request, *args, **kwargs)

    return wrapper

def home(request):
    return render(request, 'home.html')


def organization_signup(request):
    if request.method == 'POST':
        form = OrganizationSignupForm(request.POST)
        if form.is_valid():
            # Create a new user
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            # Create organization profile
            organization = Organization.objects.create(
                user=user,
                name=form.cleaned_data['name'],
                address=form.cleaned_data['address'],
                contact_email=form.cleaned_data['contact_email'],
            )
            # Log the user in
            login(request, user)
            return redirect('login')  # Redirect to login after signup
    else:
        form = OrganizationSignupForm()
    
    context = {'form': form}
    return render(request, 'organization_signup.html', context)

@payment_check_required
@studentorganizationtransaction_check_required
def student(request):
    print("SS\n")
    return render(request, 'student.html')

def superuser(request):
    return render(request, 'superuser.html')

def create_subscription(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            # Create a new Subscription object but don't save it yet
            new_subscription = form.save(commit=False)
            # Additional processing if needed before saving
            new_subscription.save()
            return redirect('superuser')  # Redirect after successful submission
    else:
        form = SubscriptionForm()

    return render(request, 'create_subscription.html', {'form': form}) 

# def organization_payment(request):
    
#     pass


from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from django.shortcuts import render, get_object_or_404
from .models import Organization, OrganizationSubscription, Transaction

def organization_view_paymenthistory(request):
    
    alert = request.GET.get('alert')
    context = {}
    user_profile = request.user
    organization = get_object_or_404(Organization, user=user_profile)

    organization_subscriptions = OrganizationSubscription.objects.filter(organization=organization)
    
    total_students = Student.objects.filter(organization=organization).count()
    subscription_data = []

    for subscription in organization_subscriptions:
        start_date = subscription.date_of_subscription
        end_date = date.today()
        months = []
        current_date = start_date
        
        while current_date <= end_date:
            month_str = current_date.strftime("%Y-%m-%d")
            date_obj = datetime.strptime(month_str, '%Y-%m-%d').date()
            transaction_exists = Transaction.objects.filter(
                organizationsubscription=subscription,
                month__month=date_obj.month,
            ).exists()

            months.append({
                'month': month_str,
                'transaction': transaction_exists
            })
            current_date += relativedelta(months=1)

        subscription_data.append({
            'subscription_id': subscription.id,
            'subscription_name': subscription.subscription.name,
            'subscription_price': subscription.subscription.price,
            'months': months
        })

    context = {
        'subscription_data': subscription_data,
        'total_students':total_students,
    }
    
    if alert == 'clear_dues':
        context['alert_message'] = 'Clear your previous dues!'
    return render(request, 'payment_history.html', context)








def student_view_paymenthistory(request):

    alert = request.GET.get('alert')
    context = {}
    if alert == 'clear_dues':
        context['alert_message'] = 'Clear your previous dues!'
        

    
    if alert == 'less_payment':
        context['alert_message'] = 'Payment should be at least 75%'
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)
    student = get_object_or_404(Student, user_profile=user_profile)
    organization = student.organization
    organization_subscriptions = OrganizationSubscription.objects.filter(organization=organization)
    
    total_students = Student.objects.filter(organization=organization).count()
    subscription_data = []

    for subscription in organization_subscriptions:
        start_date = subscription.date_of_subscription
        end_date = date.today()
        months = []
        current_date = start_date
        
        while current_date <= end_date:
            month_str = current_date.strftime("%Y-%m-%d")
            date_obj = datetime.strptime(month_str, '%Y-%m-%d').date()
            transaction_exists = Payment.objects.filter(
                student=student,
                organizationsubscription=subscription,
                month__month=date_obj.month,
            ).exists()

            months.append({
                'month': month_str,
                'transaction': transaction_exists
            })
            current_date += relativedelta(months=1)

        subscription_data.append({
            'subscription_id': subscription.id,
            'subscription_name': subscription.subscription.name,
            'subscription_price': subscription.subscription.price,
            'months': months
        })

    context['subscription_data']=subscription_data
    return render(request, 'student_payment_history.html', context)





@login_required
def make_studentpayment(request, subscription_id, month):
    if request.method == 'POST':
        subscription = get_object_or_404(OrganizationSubscription, id=subscription_id)
        user = request.user
        user_profile = get_object_or_404(UserProfile, user=user)
        student = get_object_or_404(Student, user_profile=user_profile)
        date_obj = datetime.strptime(month, '%Y-%m-%d').date()
        # Assuming the Subscription model has a price field
        amount = subscription.subscription.price

        # Create a new Transaction
        Payment.objects.create(
            organizationsubscription=subscription,
            student=student,
            month=date_obj,
            amount=amount,
            paymentdate=datetime.now().date()
        )

        # Deduct the amount from the organization's total payment
        # organization.total_payment -= amount
        # organization.save()

        return redirect('student_view_paymenthistory')




@login_required
def make_payment(request, subscription_id, month):
    if request.method == 'POST':
        subscription = get_object_or_404(OrganizationSubscription, id=subscription_id)
        organization = subscription.organization
        date_obj = datetime.strptime(month, '%Y-%m-%d').date()
        
        # Assuming the Subscription model has a price field
        amount = request.POST.get('payment_amount')
        # Create a new Transaction
        Transaction.objects.create(
            organizationsubscription=subscription,
            month=date_obj,
            amount=amount,
            paymentdate=datetime.now().date()
        )

        return redirect('organization_view_paymenthistory')


def subscribe(request):
    
    user_profile = request.user
    organization = get_object_or_404(Organization, user=user_profile)

    if request.method == 'POST':
        form = OrganizationSubscriptionForm(request.POST)
        if form.is_valid():

            
            organizationsubscription = OrganizationSubscription.objects.create(
                organization = organization,
                subscription=form.cleaned_data['subscription'],
                date_of_subscription=form.cleaned_data['date_of_subscription']
            )
            return redirect('organization')  # Redirect after creating student
        

    else:        
        form = OrganizationSubscriptionForm(initial={'organization': organization.name})
 
    return render(request, 'subscribe.html', {'form': form}) 

    


def user_login(request):
    alert = request.GET.get('alert')
    context = {}
    
    if alert == 'less_payment' or alert == 'organization_clear_dues':
        context['alert_message'] = 'Your organization does not meet the payment requirements'
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            if user.is_superuser:
                return redirect('superuser')
            elif hasattr(user, 'userprofile') and user.userprofile is not None:
                if user.userprofile.role == 'student':
                    return redirect('student')
                elif user.userprofile.role == 'organization':
                    print("AJEEB")
                    return redirect('organization')  # Redirect to appropriate view for organization
            else:
                # Handle other roles or scenarios here
                return redirect('organization')  # Redirect to login page with error message
        
        else:
            # If user is None, authentication failed
            context['alert_message'] = 'Username or password is incorrect.'
            return render(request, 'login.html', context)
    
    return render(request, 'login.html', context)

def user_logout(request):
    logout(request)
    return redirect('home')


@organizationtransaction_check_required
def organization(request):
    print("ff")
    return render(request, 'organization.html')

@login_required
def create_student(request):
    user_profile = request.user
    organization = get_object_or_404(Organization, user=user_profile)
    
    if request.method == 'POST':
        form = StudentCreationForm(request.POST)
        if form.is_valid():
            
            user = User.objects.create_user(
                username=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            user_profile=UserProfile.objects.create(
                user=user,
                role="student"
            )
            student = Student.objects.create(
                organization = organization,
                user_profile=user_profile,
                enrollment_date=form.cleaned_data['enrollment_date']
            )
            return redirect('home')  # Redirect after creating student
    else:
        form = StudentCreationForm(initial={'organization': organization.name})
    
    context = {'form': form}
    return render(request, 'create_student.html', context)