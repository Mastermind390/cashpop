from datetime import timedelta
from django.utils.timezone import now
from .models import UserLogin

def get_login_streak(user):
    logins = UserLogin.objects.filter(user=user).order_by('-login_date')

    if not logins:
        return 0  # No logins, no streak

    streak = 0
    today = now().date()

    for i, login in enumerate(logins):
        if i == 0 and login.login_date == today:
            streak += 1  # Today’s login counts as the start
        elif i > 0 and logins[i-1].login_date - login.login_date == timedelta(days=1):
            streak += 1  # Consecutive day, increase streak
        else:
            streak = 0
            break  # Streak is broken

    return streak
