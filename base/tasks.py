from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

@shared_task
def send_new_task_emails(subject, from_email, user_emails, context):
    for email in user_emails:
        if not email:
            continue
        html_content = render_to_string("base/new_task_email.html", context)
        text_content = f"A new task titled '{context['task_title']}' is available."
        msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
