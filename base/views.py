from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
from .models import UserProfile, UserTask, Task, UserAccountDetail, Withdrawal
from .streak import get_login_streak
from django.db import transaction




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

@login_required(login_url="base:login")
def dashboard(request):
    user = User.objects.get(id=request.user.id)
    userprofile = UserProfile.objects.get(user=user)
    
    # Get all approved tasks for the user
    usertask = UserTask.objects.filter(user=user, status="approved")
    total_user_task = usertask.count()
    
    # Update streaks
    streaks = get_login_streak(user)
    userprofile.streak += streaks
    # userprofile.save()
    
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
    }
    return render(request, "base/task_details.html", context)

@login_required(login_url="base:login")
def withdraw(request):
    user = request.user
    streaks = get_login_streak(user)
    userprofile = user.userprofile
    userprofile.streak += streaks
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
                messages.error(request, "Amount cannot be greater than your wallet balance")
            elif amount < 5000:
                messages.error(request, "Amount cannot be less than 5000")
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
            
            user.userprofile.balance += move_amount
            user.userprofile.task_earning -= move_amount
            user.userprofile.save()
            messages.success(request, "transfer successfully")
            return redirect("base:withdraw")


    return render(request, "base/withdraw.html", {"withdraws" : withdraws})



@login_required(login_url="base:login")
def account(request):
    state = "not-edit"
    user = request.user
    streaks = get_login_streak(user)
    request.user.userprofile.streak += streaks

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
    user_tasks = get_list_or_404(UserTask)

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
        if creator_profile.locked_balance < task.task.reward:
            messages.error(request, "Insufficient locked balance to approve this task.")
            return redirect("base:task-review")

        # 1. Approve the user task
        task.status = "approved"
        task.task.amount_tasker -= 1
        creator_profile.locked_balance -= task.task.reward
        task.save()
        task.task.save()
        creator_profile.save()

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