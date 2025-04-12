from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home, registerPage, loginPage, faqPage, dashboard, logoutPage, profile, createTask, task_details, withdraw, account, task_review, approve, reject

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
    path("account_settings", account, name="account"),
    path("task-review", task_review, name="task-review"),
    path("confirm-approve/<int:pk>", approve, name="confirm-approve"),
    path("confirm-reject/<int:pk>", reject, name="confirm-reject"),


    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
