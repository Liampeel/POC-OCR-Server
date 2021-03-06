from flask import render_template, current_app

from app.email import send_email


def send_password_reset_email(user):
    """Send email with password reset token to the given user."""
    token = user.get_reset_password_token()
    send_email.delay(
        '[Vulture] Reset Your Password',
        sender=current_app.config['ADMINS'][0],
        recipients=[user.email],
        text_body=render_template(
            'emails/reset_password.txt', user=user, token=token),
        html_body=render_template(
            'emails/reset_password.html', user=user, token=token))
