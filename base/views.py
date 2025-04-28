from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
from .models import UserProfile, UserTask, Task, UserAccountDetail, Withdrawal, Deposit
from .streak import get_login_streak
from django.db import transaction
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from .forms import PasswordResetRequestForm, SetNewPasswordForm
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
import hashlib
import hmac
import requests




def home(request):
    if request.user.is_authenticated:
        return redirect("base:dashboard")

    tasks = Task.objects.all()[:3]

    return render(request, "base/index.html", {"tasks" : tasks})


def registerPage(request):

    if request.user.is_authenticated:
        return redirect("base:dashboard")

    if request.method == 'POST':
        first_name = request.POST["first_name"].lower().strip()
        last_name = request.POST["last_name"].lower().strip()
        user_name = request.POST["user_name"].lower().strip()
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        email = request.POST["email"].lower().strip()

        if password == confirm_password:
            try:
                user = User.objects.get(username=email)
                # If we got here, it means user *does* exist
                messages.error(request, "User already exists, please login.")
                return render(request, "base/register.html")
            except User.DoesNotExist:
                # User doesn't exist, go ahead and register
                user = User.objects.create_user(
                    username=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    email=user_name 
            )
            user.save()
            login(request, user)
            return redirect("base:dashboard")
        else:
            messages.error(request, "password does not match")

    return render(request, "base/register.html")


def loginPage(request):

    if request.user.is_authenticated:
        return redirect("base:dashboard")

    if request.method == "POST":
        email = request.POST["email"].lower().strip()
        password = request.POST["password"].strip()  # Don't lowercase passwords

        # Authenticate directly
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("base:dashboard")
        else:
            messages.error(request, "Invalid email or password")

    return render(request, "base/login.html")

@login_required(login_url="base:login")
def logoutPage(request):
    logout(request)
    return redirect("base:login")

def faqPage(request):
    return render(request, "base/faq.html")

def forgot_password_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(username=email)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_link = request.build_absolute_uri(
                    f'/reset-password/{uid}/{token}/'
                )

                # Email the reset link
                send_mail(
                    subject='Password Reset Request',
                    message=f'Click the link to reset your password: {reset_link}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )
            except User.DoesNotExist:
                pass  # Don't reveal that the email doesn't exist
            return render(request, 'base/password_reset_sent.html')
    else:
        form = PasswordResetRequestForm()
    return render(request, 'base/forgot_password.html', {'form': form})


def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetNewPasswordForm(request.POST)
            if form.is_valid():
                user.set_password(form.cleaned_data['new_password'])
                user.save()
                return render(request, 'base/password_reset_complete.html')
        else:
            form = SetNewPasswordForm()
        return render(request, 'base/reset_password.html', {'form': form})
    else:
        return render(request, 'base/invalid_link.html')


@login_required(login_url="base:login")
def dashboard(request):
    user = User.objects.get(id=request.user.id)
    userprofile = UserProfile.objects.get(user=user)
    
    # Get all approved tasks for the user
    usertask = UserTask.objects.filter(user=user, status="approved")
    total_user_task = usertask.count()
    
    # Get completed task IDs
    completed_task_ids = usertask.values_list("task_id", flat=True)
    
    # Filter tasks by category
    category = request.GET.get("category", "all")
    if category == "all":
        available_tasks = Task.objects.filter(is_active=True)
    else:
        available_tasks = Task.objects.filter(is_active=True, category__icontains=category)
    
    # Exclude completed tasks
    available_tasks = available_tasks.exclude(id__in=completed_task_ids)
    
    total_tasks = Task.objects.filter(is_active=True).count()  # Or apply same category logic if you want
    total_available_tasks = available_tasks.count()

    context = {
        "user": user,
        "userprofile": userprofile,
        "total_user_task": total_user_task,
        "total_tasks": total_tasks,
        "available_tasks": available_tasks,
        "total_available_tasks": total_available_tasks
    }
    
    return render(request, "base/dashboard.html", context)


@login_required(login_url="base:login")
def profile(request):
    page = "profile"
    user = request.user
    streaks = get_login_streak(user)
    userprofile = user.userprofile
    userprofile.streak += streaks
    # userprofile.save()
    
    usertask = UserTask.objects.all()

    context = {"page" : page, "usertask" : usertask}
        
    return render(request, "base/profile.html", context)


@login_required(login_url="base:login")
def createTask(request):
    form = TaskForm()
    user = request.user
    userprofile = user.userprofile
    user_wallet_balance = userprofile.balance

    if request.method == "POST":
        user = user
        category = request.POST["category"]
        title = request.POST["title"]
        description = request.POST["description"]
        link = request.POST["link"]

        try:
            reward = int(request.POST.get("reward"))
        except (ValueError, TypeError):
            messages.error(request, "Invalid reward amount. Reward must be in Number")
            return redirect("base:create-task")

        try:
            minutes = int(request.POST.get("estimated_time_mins"))
        except (ValueError, TypeError):
            messages.error(request, "must be number")
            return redirect("base:create-task")

        try:
            quantity = int(request.POST.get("amount_tasker"))
        except (ValueError, TypeError):
            messages.error(request, "Invalid amount")
            return redirect("base:create-task")

        task_order = reward * quantity

        if user_wallet_balance < task_order:
            messages.error(request, "insufficient amount in wallet. Please! deposit to continue")
            return redirect("base:create-task")
        elif task_order <= 0:
            messages.error(request, "amount of workers or how much you are willing to pay must be greater than 0")
            return redirect("base:create-task")
        else:
            task = Task.objects.create(
            creator= user,
            category=category,
            title = title,
            description = description,
            link = link,
            estimated_time_mins = minutes,
            reward = reward,
            amount_tasker = quantity,
            is_active = True
            )
            task.save()
            userprofile.balance -= task_order
            userprofile.locked_balance += task_order
            userprofile.save()
            return redirect("base:dashboard")

    return render(request, "base/create_task.html", {"form" : form})


@login_required(login_url="base:login")
def task_details(request, pk):
    task = get_object_or_404(Task, title=pk)
    user = User.objects.get(id=request.user.id)
    usertask = UserTask.objects.filter(user=user, status="pending")
    pending_task_ids = usertask.values_list("task_id", flat=True)

    if request.method == "POST":
        proof_username = request.POST.get("proof")
        proof_image = request.FILES.get("screenshot")

        submitted_task = UserTask.objects.create(
            user = request.user,
            task = task,
            proof_image = proof_image,
            proof_username = proof_username,
            status = "pending"
        )
        submitted_task.save()
        return redirect("base:dashboard")

    context = {
        "task" : task,
        "pending_task_ids" : pending_task_ids,
    }
    return render(request, "base/task_details.html", context)

@login_required(login_url="base:login")
def deposit(request):

    return render(request, "base/deposit.html")

@login_required(login_url="base:login")
def withdraw(request):
    user = request.user
    # streaks = get_login_streak(user)
    # userprofile = user.userprofile
    # userprofile.streak += streaks
    # userprofile.save()
    withdraws = Withdrawal.objects.all()

    if request.method == "POST":
        action = request.POST.get("action")
        user_balance = user.userprofile.balance
       

        if action == "withdraw":
            try:
                amount = int(request.POST.get("amount"))
            except (ValueError, TypeError):
                messages.error(request, "Invalid amount")
                return redirect("base:withdraw")
        
            if amount > user_balance:
                messages.error(request, "insufficient wallet balance")
                return redirect("base:withdraw")
            elif amount < 5000:
                messages.error(request, "Amount cannot be less than 5000")
                return redirect("base:withdraw")
            else:
                withdraw = Withdrawal.objects.create(user=user, amount=amount, status="pending")
                withdraw.save()
                messages.success(request, "withdrawer request submited")
                return redirect("base:withdraw")
        else:
            try:
                move_amount = int(request.POST.get("move_amount"))
            except (ValueError, TypeError):
                messages.error(request, "Invalid amount")
                return redirect("base:withdraw")
            
            if user.userprofile.task_earning >= move_amount:
                user.userprofile.balance += move_amount
                user.userprofile.task_earning -= move_amount
                user.userprofile.save()
                messages.success(request, "transfer successfully")
                return redirect("base:withdraw")
            else:
                 messages.error(request, "insufficient balance")
                 return redirect("base:withdraw")


    return render(request, "base/withdraw.html", {"withdraws" : withdraws})


@login_required(login_url="base:login")
def account(request):
    state = "not-edit"
    user = request.user
    # streaks = get_login_streak(user)
    # request.user.userprofile.streak += streaks

    try:
        account_detail = UserAccountDetail.objects.get(user=user)
    except UserAccountDetail.DoesNotExist:
        account_detail = None

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        account_number = request.POST.get("account_number")
        bank_name = request.POST.get("bank_name")

        UserAccountDetail.objects.update_or_create(
            user = request.user,
            bank_name = bank_name,
            account_number = account_number,
            full_name = full_name
        )
       
        state = "edit"
        return redirect("base:dashboard")


    context = {
        "state" : state,
        "account_detail": account_detail
    }
    return render(request, "base/account_settings.html", context)

@login_required(login_url="base:login")
def task_review(request):
    user_tasks = UserTask.objects.filter(task__creator=request.user)

    user = request.user
    streaks = get_login_streak(user)
    request.user.userprofile.streak += streaks
    return render(request, "base/task_review.html", {"user_tasks" : user_tasks})


@transaction.atomic
@login_required(login_url="base:login")
def approve(request, pk):
    task = get_object_or_404(UserTask, id=pk)

    if request.method == "POST":
        # Lock the row to prevent concurrent updates
        task = UserTask.objects.select_for_update().get(id=pk)

        # Prevent duplicate approval
        # if task.status != "pending":
        #     messages.warning(request, "This task has already been reviewed.")
        #     return redirect("base:task-review")

        # Check if the task still has available slots
        if task.task.amount_tasker <= 0:
            task.task.is_active=False
            messages.error(request, "No available slots left for this task.")
            return redirect("base:task-review")

        # Check if the creator has enough locked balance
        creator_profile = task.task.creator.userprofile
        # if creator_profile.locked_balance < task.task.reward:
        #     messages.error(request, "Insufficient locked balance to approve this task.")
        #     return redirect("base:task-review")

        # 1. Approve the user task
        task.status = "approved"
        # task.task.amount_tasker -= 1
        task.task.num_of_completed += 1
        creator_profile.locked_balance -= task.task.reward
        task.save()
        task.task.save()
        creator_profile.save()

        if task.task.num_of_completed >= task.task.amount_tasker:
            task.task.is_active = False

        # 2. Update the user profile earnings
        user_profile = task.user.userprofile
        user_profile.task_earning += task.task.reward
        user_profile.total_task_completed += 1
        user_profile.total_reward += task.task.reward
        user_profile.save()

        messages.success(request, "Task approved successfully!")
        return redirect("base:task-review")

    return render(request, "base/approve.html", {"task": task})

@login_required(login_url="base:login")
def reject(request, pk):
    task = get_object_or_404(UserTask, id=pk)

    if request.method == "POST":
        task.status = "rejected"
        task.save()
        return redirect("base:task-review")
    return render(request, "base/task_review.html", {"task" : task})


def initialize_payment(request):
    if request.method == 'POST':
        amount = int(request.POST.get('amount'))
        email = request.user.username  # or however you want to get the email

        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }

        data = {
            "email": email,
            "amount": amount * 100,  # Paystack works in kobo
            "callback_url": "https://c00c-102-134-16-210.ngrok-free.app/webhook/paystack/",
        }

        response = requests.post('https://api.paystack.co/transaction/initialize', headers=headers, json=data)
        response_data = response.json()

        if response_data.get('status'):
            payment_url = response_data['data']['authorization_url']
            return redirect(payment_url)
        else:
            return JsonResponse({'error': 'Payment initialization failed'}, status=400)



@csrf_exempt
@login_required(login_url="base:login")
def paystack_webhook(request):
    print("webhook triggered")
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request")

    secret = settings.PAYSTACK_SECRET_KEY.encode('utf-8')
    signature = request.headers.get('x-paystack-signature')
    payload = request.body
    computed_signature = hmac.new(secret, msg=payload, digestmod=hashlib.sha512).hexdigest()

    print(signature)
    print(computed_signature)

    if signature != computed_signature:
        return HttpResponseBadRequest("Invalid signature")

    data = json.loads(payload)
    event = data.get('event')

    if event == 'charge.success':
        payment_data = data['data']
        reference = payment_data['reference']
        amount_paid = int(payment_data['amount']) // 100  # Convert from kobo to naira

        try:
            deposit = Deposit.objects.get(reference=reference, status='pending')
            deposit.status = 'completed'
            deposit.save()

            # Update user balance
            profile = UserProfile.objects.get(user=deposit.user)
            profile.balance += amount_paid
            profile.save()

        except Deposit.DoesNotExist:
            return JsonResponse({'error': 'Deposit not found'}, status=404)

    return JsonResponse({'status': 'success'}, status=200)


@login_required(login_url="base:login")
def userTasksview(request):
    user = request.user
    tasks = Task.objects.filter(creator=user)

    context = {
        "tasks" : tasks,
    }

    return render(request, "base/user_task_view.html", context)