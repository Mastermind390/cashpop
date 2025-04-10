from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
from .models import UserProfile, UserTask, Task, UserAccountDetail, Withdrawal
from .streak import get_login_streak




def home(request):

    if request.user.is_authenticated:
        return redirect("base:dashboard")

    return render(request, "base/index.html")


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
            except:
                messages.error(request, "user already exist")
                return render(request, "base/register.html")
            finally:
                user = User.objects.create_user(
                    username=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    email=user_name
                )
                user.save()
                login(request, user)
                return render(request, "base/dashboard.html")
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


def logoutPage(request):
    logout(request)
    return redirect("base:login")

def faqPage(request):
    return render(request, "base/faq.html")

@login_required(login_url="base:login")
def dashboard(request):
    user = User.objects.get(id=request.user.id)
    userprofile = UserProfile.objects.get(id=user.id)
    usertask = UserTask.objects.filter(status="approved")
    total_user_task = usertask.count()
    streaks = get_login_streak(user)
    request.user.userprofile.streak += streaks
    
    available_tasks = Task.objects.filter(is_active=True)
    


    category = request.GET.get("category", "all")
    if category == "all":
        total_tasks = Task.objects.all()
    else:
        total_tasks = Task.objects.filter(category__icontains=category)

    completed_task_ids = usertask.filter(status="approved").values_list("task_id", flat=True)

    available_tasks = available_tasks.exclude(id__in=completed_task_ids)
    total_available_tasks = available_tasks.count()

    context = {
        "user" : user, 
        "userprofile":userprofile, 
        "total_user_task" : total_user_task,
        "total_tasks" : total_tasks,
        "available_tasks" : available_tasks,
        "total_available_tasks" : total_available_tasks
        }
    return render(request, "base/dashboard.html", context)


@login_required(login_url="base:login")
def profile(request):
    page = "profile"
    user = request.user
    streaks = get_login_streak(user)
    streaks = get_login_streak(user)
    request.user.userprofile.streak += streaks
    
    usertask = UserTask.objects.all()

    context = {"page" : page, "usertask" : usertask}
        
    return render(request, "base/profile.html", context)


@login_required(login_url="base:login")
def createTask(request):
    form = TaskForm()

    if request.method == "POST":
        user = request.user
        category = request.POST["category"]
        title = request.POST["title"]
        description = request.POST["description"]
        link = request.POST["link"]
        time = request.POST["estimated_time_mins"]
        reward = request.POST["reward"]

        task = Task.objects.create(
            creator= user,
            category=category,
            title = title,
            description = description,
            link = link,
            estimated_time_mins = time,
            reward = reward,
            is_active = True
        )
        task.save()
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
    request.user.userprofile.streak += streaks
    withdraws = Withdrawal.objects.all()

    if request.method == "POST":
        amount = request.POST.get("amount")

        withdraw = Withdrawal.objects.create(
            user = user,
            amount = amount,
            status = "pending"
        )
        withdraw.save()
        return redirect("base:withdraw")



    return render(request, "base/withdraw.html", {"withdraws" : withdraws})



@login_required(login_url="base:login")
def account(request):
    state = "not-edit"
    user = request.user
    streaks = get_login_streak(user)
    request.user.userprofile.streak += streaks

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
        "state" : state
    }
    return render(request, "base/account_settings.html", context)


def task_review(request):
    user_tasks = get_list_or_404(UserTask)

    user = request.user
    streaks = get_login_streak(user)
    request.user.userprofile.streak += streaks
    return render(request, "base/task_review.html", {"user_tasks" : user_tasks})


def approve(request, pk):
    task = get_object_or_404(UserTask, id=pk)
    user = request.user.id

    if request.method == "POST":
        # 1. Update the UserTask status
        task.status = "approved"
        task.save()

        # 2. Update the user's profile earnings
        user_profile = task.user.userprofile
        user_profile.task_earning += task.task.reward
        user_profile.total_task_completed += 1
        user_profile.total_reward += task.task.reward
        user_profile.save()
    
        return redirect("base:task-review")
        

    return render(request, "base/approve.html", {"task" : task})


def reject(request, pk):
    task = get_object_or_404(UserTask, id=pk)

    if request.method == "POST":
        task.status = "rejected"
        task.save()
        return redirect("base:task-review")
    return render(request, "base/task_review.html", {"user_tasks" : user_tasks})