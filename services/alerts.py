"""
Alerts Service
Handles sending SMS via Twilio and Emails via Flask-Mail asynchronously using Celery
"""

import os
import logging
from flask_mail import Message
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from extensions import mail

logger = logging.getLogger(__name__)

# Placeholder for Celery task decorator
# @celery.task
def send_email_alert_async(subject, recipient, body):
    """Send email asynchronously (Simulated via function call for now until celery is wired)"""
    from app import create_app
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    with app.app_context():
        try:
            msg = Message(subject,
                          sender=app.config.get('MAIL_DEFAULT_SENDER', 'noreply@smartassist.com'),
                          recipients=[recipient])
            msg.body = body
            mail.send(msg)
            logger.info(f"Email sent successfully to {recipient}")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")

# @celery.task
def send_sms_alert_async(to_number, message_body):
    """Send SMS via Twilio asynchronously"""
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    from_number = os.environ.get('TWILIO_FROM_NUMBER')

    if not all([account_sid, auth_token, from_number]):
        logger.warning("Twilio credentials missing. SMS not sent.")
        return False

    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=message_body,
            from_=from_number,
            to=to_number
        )
        logger.info(f"SMS sent successfully: {message.sid}")
        return True
    except TwilioRestException as e:
        logger.error(f"Twilio API Error: {e}")
        return False
    except Exception as e:
        logger.error(f"Failed to send SMS: {e}")
        return False

def broadcast_emergency(title, message, users):
    """Send broadcast to multiple users"""
    for user in users:
        if user.email:
            send_email_alert_async(f"EMERGENCY ALERT: {title}", user.email, message)
        # If user has phone number in DB:
        # send_sms_alert_async(user.phone, message)
