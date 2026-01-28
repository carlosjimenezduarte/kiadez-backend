import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.core.config import settings


def send_verification_email(to_email: str, token: str) -> None:
    verify_url = f"{settings.BACKEND_URL}/auth/verify-email?token={token}"

    subject = "Verifica tu correo electrónico en Kiadez"

    html_body = f"""
    <!DOCTYPE html>
    <html lang="es">

    <head>
    <meta charset="UTF-8">
    <title>Verifica tu correo · Kiadez</title>
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
                    Bienvenido a Kiadez
                </h2>

                <p style="text-align:center; font-size:15px; line-height:1.6;">
                    Gracias por registrarte en <strong>Kiadez</strong>.
                    Para continuar y activar tu cuenta, confirma tu dirección de correo electrónico.
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
                    Verificar correo
                    </a>
                </div>

                <p style="text-align:center; font-size:14px; color:#555;">
                    Si no solicitaste esta cuenta, puedes ignorar este mensaje.
                </p>

                <hr style="border:none; border-top:1px solid #e0e0e0; margin:30px 0;">

                <p style="font-size:12px; color:#777; text-align:center;">
                    Kiadez · Ingeniería de la Conciencia<br>
                    Una red social para cumplir deseos
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

    subject = "Restablece tu contraseña en Kiadez"

    html_body = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
    <meta charset="UTF-8">
    <title>Restablecer contraseña · Kiadez</title>
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
                    Restablece tu contraseña
                </h2>

                <p style="text-align:center; font-size:15px; line-height:1.6;">
                    Recibimos una solicitud para cambiar tu contraseña. Si fuiste tú, usa el botón de abajo.
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
                    Restablecer contraseña
                    </a>
                </div>

                <p style="text-align:center; font-size:14px; color:#555;">
                    Si no solicitaste este cambio, puedes ignorar este mensaje.
                </p>

                <hr style="border:none; border-top:1px solid #e0e0e0; margin:30px 0;">

                <p style="font-size:12px; color:#777; text-align:center;">
                    Kiadez · Ingeniería de la Conciencia<br>
                    Una red social para cumplir deseos
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
    subject = f"Nuevo mensaje de contacto: {name}"

    html_body = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
    <meta charset="UTF-8">
    <title>Contacto · Kiadez</title>
    </head>
    <body style="font-family: Arial, Helvetica, sans-serif; color:#1e1e1e;">
      <h2>Nuevo mensaje de contacto</h2>
      <p><strong>Nombre:</strong> {name}</p>
      <p><strong>Email:</strong> {email}</p>
      <p><strong>Mensaje:</strong></p>
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
