from django.urls import path
from .views import home, registerPage, loginPage, faqPage, dashboard, logoutPage, profile, createTask, task_details, payment_history, account

app_name = 'base'

urlpatterns = [
    path("", home, name="home"),
    path("register/", registerPage, name="register"),
    path("login/", loginPage, name="login"),
    path("logout/", logoutPage, name="logout"),
    path("faq/", faqPage, name="faq"),
    path("dashboard/", dashboard, name="dashboard"),
    path("profile/", profile, name="profile"),
    path("create-task/", createTask, name="create-task"),
    path("task-details/<str:pk>", task_details, name="task-details"),
    path("payment-history/", payment_history, name="payment-history"),
    path("account_settings", account, name="account"),

]
