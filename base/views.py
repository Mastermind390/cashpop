from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
from .models import UserProfile, UserTask, Task
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
    usertask = UserTask.objects.all()
    total_user_task = usertask.count()
    streaks = get_login_streak(user)
    request.user.userprofile.streak += streaks
    
    available_tasks = Task.objects.all()
    total_available_tasks = 0

    for task in available_tasks:
        if task.is_active:
            total_available_tasks+=1


    request.GET.get('q') if request.GET.get("q") != None else ""
    category = request.GET.get("category", "all")
    if category == "all":
        total_tasks = Task.objects.all()
    else:
        total_tasks = Task.objects.filter(category__icontains=category)

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

    user_profile = request.user.userprofile
    user_profile.streak += streaks
    user_profile.save()
    
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


def payment_history(request):
    user = request.user
    streaks = get_login_streak(user)
    request.user.userprofile.streak += streaks
    return render(request, "base/payment_history.html")


def account(request):
    state = "edit"
    user = request.user
    streaks = get_login_streak(user)
    request.user.userprofile.streak += streaks
    context = {
        "state" : state
    }
    return render(request, "base/account_settings.html", context)
