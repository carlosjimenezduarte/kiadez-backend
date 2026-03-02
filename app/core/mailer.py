import smtplib
import html
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.core.config import settings


def send_verification_email(to_email: str, token: str) -> None:
    verify_url = f"{settings.BACKEND_URL}/auth/verify-email?token={token}"

    subject = "Verify your email in Kiadez"

    html_body = f"""
    <!DOCTYPE html>
    <html lang="en">

    <head>
    <meta charset="UTF-8">
    <title>Verify your email · Kiadez</title>
    </head>

    <body style="
    margin:0;
    padding:0;
    background-color:#0e1a14;
    font-family: Arial, Helvetica, sans-serif;
    color:#1e1e1e;
    ">

    <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#0e1a14; padding:40px 0;">
        <tr>
        <td align="center">

            <table width="600" cellpadding="0" cellspacing="0" style="
            background:#ffffff;
            border-radius:12px;
            overflow:hidden;
            ">

            <!-- Header -->
            <tr>
                <td align="center" style="
                background:#00674F;
                padding:30px;
                ">
                <img src="https://kiadez.com/assets/logo-email.png" alt="Kiadez" width="120" style="display:block;" />
                </td>
            </tr>

            <!-- Body -->
            <tr>
                <td style="padding:35px;">
                <h2 style="text-align:center; margin-top:0; color:#1e1e1e;">
                    Welcome to Kiadez
                </h2>

                <p style="text-align:center; font-size:15px; line-height:1.6;">
                    Thanks for signing up at <strong>Kiadez</strong>.
                    To continue and activate your account, confirm your email address.
                </p>

                <div style="text-align:center; margin:30px 0;">
                    <a href="{verify_url}" style="
                        display:inline-block;
                        padding:14px 28px;
                        background:#00674F;
                        color:#ffffff;
                        text-decoration:none;
                        border-radius:8px;
                        font-weight:bold;
                        font-size:15px;
                    ">
                    Verify email
                    </a>
                </div>

                <p style="text-align:center; font-size:14px; color:#555;">
                    If you did not request this account, you can ignore this message.
                </p>

                <hr style="border:none; border-top:1px solid #e0e0e0; margin:30px 0;">

                <p style="font-size:12px; color:#777; text-align:center;">
                    Kiadez · Consciousness Engineering<br>
                    A social network to fulfill wishes
                </p>
                </td>
            </tr>

            </table>

        </td>
        </tr>
    </table>

    </body>

    </html>
    """


    msg = MIMEMultipart("alternative")
    msg["From"] = settings.SMTP_FROM
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(html_body, "html"))

    # SSL directo (Hostinger suele ser 465)
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, timeout=20) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)


def send_password_reset_email(to_email: str, token: str) -> None:
    reset_url = f"{settings.FRONTEND_URL}/reset-password.html?token={token}"
    expires_minutes = settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES

    subject = "Reset your password in Kiadez"

    html_body = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <title>Reset password · Kiadez</title>
    </head>
    <body style="
    margin:0;
    padding:0;
    background-color:#0e1a14;
    font-family: Arial, Helvetica, sans-serif;
    color:#1e1e1e;
    ">

    <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#0e1a14; padding:40px 0;">
        <tr>
        <td align="center">

            <table width="600" cellpadding="0" cellspacing="0" style="
            background:#ffffff;
            border-radius:12px;
            overflow:hidden;
            ">

            <tr>
                <td align="center" style="
                background:#00674F;
                padding:30px;
                ">
                <img src="https://kiadez.com/assets/logo-email.png" alt="Kiadez" width="120" style="display:block;" />
                </td>
            </tr>

            <tr>
                <td style="padding:35px;">
                <h2 style="text-align:center; margin-top:0; color:#1e1e1e;">
                    Reset your password
                </h2>

                <p style="text-align:center; font-size:15px; line-height:1.6;">
                    We received a request to change your password. If it was you, use the button below.
                </p>

                <div style="text-align:center; margin:30px 0;">
                    <a href="{reset_url}" style="
                        display:inline-block;
                        padding:14px 28px;
                        background:#00674F;
                        color:#ffffff;
                        text-decoration:none;
                        border-radius:8px;
                        font-weight:bold;
                        font-size:15px;
                    ">
                    Reset password
                    </a>
                </div>

                <p style="text-align:center; font-size:14px; color:#555;">
                    This link will expire in <strong>{expires_minutes} minutes</strong> for security reasons.
                </p>

                <p style="text-align:center; font-size:12px; color:#777; word-break: break-all; margin:18px 0 0;">
                    If the button does not work, copy and paste this link into your browser:<br />
                    <a href="{reset_url}" style="color:#00674F; text-decoration:none;">{reset_url}</a>
                </p>

                <p style="text-align:center; font-size:14px; color:#555;">
                    If you did not request this change, you can ignore this message.
                </p>

                <hr style="border:none; border-top:1px solid #e0e0e0; margin:30px 0;">

                <p style="font-size:12px; color:#777; text-align:center;">
                    Kiadez · Consciousness Engineering<br>
                    A social network to fulfill wishes
                </p>
                </td>
            </tr>

            </table>

        </td>
        </tr>
    </table>

    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["From"] = settings.SMTP_FROM
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, timeout=20) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)


def send_email_change_confirmation_email(*, to_email: str, previous_email: str) -> None:
    subject = "Your email was updated in Kiadez"

    html_body = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <title>Email change · Kiadez</title>
    </head>
    <body style="
    margin:0;
    padding:0;
    background-color:#0e1a14;
    font-family: Arial, Helvetica, sans-serif;
    color:#1e1e1e;
    ">

    <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#0e1a14; padding:40px 0;">
        <tr>
        <td align="center">

            <table width="600" cellpadding="0" cellspacing="0" style="
            background:#ffffff;
            border-radius:12px;
            overflow:hidden;
            ">

            <tr>
                <td align="center" style="
                background:#00674F;
                padding:30px;
                ">
                <img src="https://kiadez.com/assets/logo-email.png" alt="Kiadez" width="120" style="display:block;" />
                </td>
            </tr>

            <tr>
                <td style="padding:35px;">
                <h2 style="text-align:center; margin-top:0; color:#1e1e1e;">
                    Email updated
                </h2>

                <p style="text-align:center; font-size:15px; line-height:1.6;">
                    We confirm that your sign-in email in <strong>Kiadez</strong> was updated successfully.
                </p>

                <p style="text-align:center; font-size:14px; color:#555; margin:20px 0 0;">
                    Previous email: <strong>{previous_email}</strong><br />
                    Current email: <strong>{to_email}</strong>
                </p>

                <p style="text-align:center; font-size:14px; color:#555;">
                    If you did not authorize this change, please contact support immediately.
                </p>

                <hr style="border:none; border-top:1px solid #e0e0e0; margin:30px 0;">

                <p style="font-size:12px; color:#777; text-align:center;">
                    Kiadez · Consciousness Engineering<br>
                    A social network to fulfill wishes
                </p>
                </td>
            </tr>

            </table>

        </td>
        </tr>
    </table>

    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["From"] = settings.SMTP_FROM
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, timeout=20) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)


def send_email_change_security_alert_email(*, to_email: str, new_email: str) -> None:
    subject = "Security alert: email change in Kiadez"

    html_body = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <title>Security alert · Kiadez</title>
    </head>
    <body style="
    margin:0;
    padding:0;
    background-color:#0e1a14;
    font-family: Arial, Helvetica, sans-serif;
    color:#1e1e1e;
    ">

    <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#0e1a14; padding:40px 0;">
        <tr>
        <td align="center">

            <table width="600" cellpadding="0" cellspacing="0" style="
            background:#ffffff;
            border-radius:12px;
            overflow:hidden;
            ">

            <tr>
                <td align="center" style="
                background:#00674F;
                padding:30px;
                ">
                <img src="https://kiadez.com/assets/logo-email.png" alt="Kiadez" width="120" style="display:block;" />
                </td>
            </tr>

            <tr>
                <td style="padding:35px;">
                <h2 style="text-align:center; margin-top:0; color:#1e1e1e;">
                    Security alert
                </h2>

                <p style="text-align:center; font-size:15px; line-height:1.6;">
                    Your sign-in email in <strong>Kiadez</strong> was changed recently.
                </p>

                <p style="text-align:center; font-size:14px; color:#555; margin:20px 0 0;">
                    New configured email: <strong>{new_email}</strong>
                </p>

                <p style="text-align:center; font-size:14px; color:#555;">
                    If you did not authorize this change, contact support immediately.
                </p>

                <hr style="border:none; border-top:1px solid #e0e0e0; margin:30px 0;">

                <p style="font-size:12px; color:#777; text-align:center;">
                    Kiadez · Consciousness Engineering<br>
                    A social network to fulfill wishes
                </p>
                </td>
            </tr>

            </table>

        </td>
        </tr>
    </table>

    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["From"] = settings.SMTP_FROM
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, timeout=20) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)


def send_minor_account_accreditation_email(
    *,
    to_email: str,
    minor_username: str,
    minor_email: str,
    registration_date_label: str,
    approval_url: str,
) -> None:
    subject = "Minor account validation on Kiadez.com"

    safe_minor_username = html.escape(minor_username or "User")
    safe_minor_email = html.escape(minor_email or "")
    safe_registration_date = html.escape(registration_date_label or "")
    safe_approval_url = html.escape(approval_url or "")

    html_body = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <title>Minor account validation · Kiadez</title>
    </head>
    <body style="
    margin:0;
    padding:0;
    background-color:#0e1a14;
    font-family: Arial, Helvetica, sans-serif;
    color:#1e1e1e;
    ">

    <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#0e1a14; padding:40px 0;">
        <tr>
        <td align="center">

            <table width="600" cellpadding="0" cellspacing="0" style="
            background:#ffffff;
            border-radius:12px;
            overflow:hidden;
            ">

            <tr>
                <td align="center" style="
                background:#00674F;
                padding:30px;
                ">
                <img src="https://kiadez.com/assets/logo-email.png" alt="Kiadez" width="120" style="display:block;" />
                </td>
            </tr>

            <tr>
                <td style="padding:35px;">
                <p style="font-size:15px; line-height:1.7; margin:0 0 14px;">
                    Dear,
                </p>

                <p style="font-size:15px; line-height:1.7; margin:0 0 14px;">
                    We inform you that the user <strong>{safe_minor_username}</strong>, associated with the email
                    <strong>{safe_minor_email}</strong>, registered on Kiadez.com on
                    <strong>{safe_registration_date}</strong>.
                </p>

                <p style="font-size:15px; line-height:1.7; margin:0 0 14px;">
                    According to the information provided during registration, the user is a minor,
                    therefore their account is currently in protected mode.
                </p>

                <p style="font-size:15px; line-height:1.7; margin:0 0 14px;">
                    This means the user can use the platform, but their content will remain private and will not be
                    publicly visible until validated by a responsible adult.
                </p>

                <p style="font-size:15px; line-height:1.7; margin:0 0 14px;">
                    If you authorize the minor under your responsibility to enable public features within
                    the platform, you can approve it by clicking the following link:
                </p>

                <div style="text-align:center; margin:26px 0;">
                    <a href="{safe_approval_url}" style="
                        display:inline-block;
                        padding:14px 28px;
                        background:#00674F;
                        color:#ffffff;
                        text-decoration:none;
                        border-radius:8px;
                        font-weight:bold;
                        font-size:15px;
                    ">
                    Approve validation
                    </a>
                </div>

                <p style="font-size:15px; line-height:1.7; margin:0 0 14px;">
                    If public enablement is not approved, the account will continue operating in private mode.
                    You may also manage additional privacy settings from your corresponding panel.
                </p>

                <p style="font-size:15px; line-height:1.7; margin:0 0 14px;">
                    Kiadez promotes the responsible and supervised use of technology for minors.
                </p>

                <p style="font-size:15px; line-height:1.7; margin:0;">
                    Sincerely,<br />
                    Kiadez Team
                </p>

                <p style="font-size:12px; line-height:1.6; color:#6b6b6b; margin:18px 0 0; word-break:break-all;">
                    If the button does not work, copy and paste this link into your browser:<br />
                    <a href="{safe_approval_url}" style="color:#00674F; text-decoration:none;">{safe_approval_url}</a>
                </p>
                </td>
            </tr>

            </table>

        </td>
        </tr>
    </table>

    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["From"] = settings.SMTP_FROM
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, timeout=20) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)


def send_contact_email(*, name: str, email: str, message: str) -> None:
    subject = f"New contact message: {name}"

    html_body = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <title>Contact · Kiadez</title>
    </head>
    <body style="font-family: Arial, Helvetica, sans-serif; color:#1e1e1e;">
      <h2>New contact message</h2>
      <p><strong>Name:</strong> {name}</p>
      <p><strong>Email:</strong> {email}</p>
      <p><strong>Message:</strong></p>
      <p>{message}</p>
    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["From"] = settings.SMTP_FROM
    msg["To"] = settings.SUPPORT_EMAIL
    msg["Subject"] = subject
    msg.add_header("Reply-To", email)
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, timeout=20) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)
