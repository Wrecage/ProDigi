from celery import shared_task
from django.utils import timezone
from datetime import datetime

@shared_task
def send_reminder_notification(entry_id, entry_title, reminder_date, reminder_time):
    current_datetime = timezone.now()
    reminder_datetime = datetime.combine(reminder_date, reminder_time)

    # Check if the reminder date and time have passed
    if current_datetime >= reminder_datetime:
        # Send notification (implement your notification logic here)
        notification_message = f"Reminder for entry #{entry_id}: {entry_title}"
        print(notification_message)  # Replace this with your actual notification logic
