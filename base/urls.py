from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import home, registerPage, loginPage, faqPage, dashboard, logoutPage, profile, createTask, task_details, withdraw, deposit, account, task_review, approve, reject, reset_password, forgot_password_request, paystack_webhook, initialize_payment, userTasksview, activate,  paystack_success, paystack_failure

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
    path("withdraw/", withdraw, name="withdraw"),
    path("deposit/", deposit, name="deposit"),
    path("account_settings", account, name="account"),
    path("task-review", task_review, name="task-review"), 
    path("task-views", userTasksview, name="task-views"),
    path("confirm-approve/<int:pk>", approve, name="confirm-approve"),
    path("confirm-reject/<int:pk>", reject, name="confirm-reject"),
    path('forgot-password/', forgot_password_request, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', reset_password, name='reset_password'),
    path('webhook/paystack/', paystack_webhook, name='paystack_webhook'),
    path("initialize_payment/", initialize_payment, name="initialize_payment"),
    path("payment_successful/", paystack_success, name="payment_successful"), 
    path("payment_failed/", paystack_failure, name="payment_failed"),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
]
