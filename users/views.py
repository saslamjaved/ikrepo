from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage

from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, PasswordChangeForm

from .forms import CustomUserCreationForm,  UserProfileUpdateForm
from .models import CustomUser
from .tokens import account_activation_token
from subscriptions.models import UserSubscription

User = get_user_model()
token_generator = PasswordResetTokenGenerator()


# Create your views here.
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        fname = request.POST["first_name"]
        lname = request.POST["last_name"]
        email = request.POST["email"]
        pass1 = request.POST["password1"]
        pass2 = request.POST["password2"]

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('users:register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('users:register')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('users:register')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('users:register')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('users:register')
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.fname = fname
        myuser.lname = lname
        # myuser.is_active = False
        myuser.is_active = False
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")
        
        # Welcome Email
        subject = "Welcome to ikSaan.com Login!!"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to ikSaan.com! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nikAdmin"        
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        
        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ ikSaan.com  Login!!"
        message2 = render_to_string('account/email_confirmation.html',{
            
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': token_generator.make_token(myuser),
        })
        print("{{{{{{{{{{{EMail}}}}}}}}}}}")
        print(message2)
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
        )
        send_mail(email_subject, message2, from_email, to_list, fail_silently=True)
        return redirect('users:login')
    return render(request, "account/register.html")


def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and default_token_generator.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        auth_login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('users:login')
    else:
        return render(request,'account/activation_invalid.html')


def test_email(request):
    try:
        send_mail(
            'Test Email',
            'Email confirmation testing.',
            'iksaangroups@gmail.com',
            ['sdaslamjaveed@gmail.com'],
            fail_silently=False,
        )
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")
    return render(request,'account/registration_complete.html')

@login_required
def profile_update(request):
    user_subscription_details = UserSubscription.objects.filter(user=request.user).first()
    if UserSubscription.objects.filter(user=request.user, plan__name='gold', is_active=True).exists():
        user_subscription="gold"
    elif UserSubscription.objects.filter(user=request.user, plan__name='silver', is_active=True).exists():
        user_subscription="silver"
    elif UserSubscription.objects.filter(user=request.user, plan__name='bronze', is_active=True).exists()    :
        user_subscription="bronze"
    else:
        user_subscription=None

    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('users:profile')
    else:
        form = UserProfileUpdateForm(instance=request.user)
    
    return render(request, 'account/profile.html', {'form': form,'user_subscription':user_subscription,'usd':user_subscription_details})



def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'account/login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('home')

def user_changepass(request):
    if request.method == "POST":
        fm = SetPasswordForm(user = request.user, data=request.POST)
        if fm.is_valid():
            fm.save()
            update_session_auth_hash(request,fm.user)
            messages.success(request," Password Changed successfully !!..")
            return redirect('users:profile')
    else:
        fm = SetPasswordForm(user = request.user)
    return render(request,'account/password_reset.html', {"form":fm})

# Password Reset Request View
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            associated_users = get_user_model().objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    # Send email with password reset link
                    subject = "Password Reset Requested"
                    email_template_name = "account/password_reset_email.html"
                    c = {
                        "email": user.email,
                        'domain': request.get_host(),
                        'site_name': 'ikSaan.com',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email_body = render_to_string(email_template_name, c)
                    send_mail(subject, email_body, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
            return redirect("users:password_reset_done")
    else:
        form = PasswordResetForm()
    return render(request, "account/password_reset_form.html", {"form": form})

# Password Reset Done View
def password_reset_done(request):
    return render(request, "account/password_reset_done.html")

# Password Reset Confirm View
def password_reset_confirm(request, uidb64=None, token=None):
    UserModel = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserModel._default_manager.get(pk=uid)
        if not default_token_generator.check_token(user, token):
            return redirect('users:password_reset_invalid')
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            auth_login(request, user)
            return redirect('users:password_reset_complete')
    else:
        form = SetPasswordForm(user)

    return render(request, 'account/password_reset_confirm.html', {'form': form})

# Password Reset Complete View
def password_reset_complete(request):
    return render(request, 'account/password_reset_complete.html')

# Password Reset Invalid View (for invalid token)
def password_reset_invalid(request):
    return render(request, 'account/password_reset_invalid.html')