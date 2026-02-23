import smtplib
import html
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
    expires_minutes = settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES

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
                    Este enlace expirará en <strong>{expires_minutes} minutos</strong> por seguridad.
                </p>

                <p style="text-align:center; font-size:12px; color:#777; word-break: break-all; margin:18px 0 0;">
                    Si el botón no funciona, copia y pega este enlace en tu navegador:<br />
                    <a href="{reset_url}" style="color:#00674F; text-decoration:none;">{reset_url}</a>
                </p>

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


def send_email_change_confirmation_email(*, to_email: str, previous_email: str) -> None:
    subject = "Tu correo fue actualizado en Kiadez"

    html_body = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
    <meta charset="UTF-8">
    <title>Cambio de correo · Kiadez</title>
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
                    Correo actualizado
                </h2>

                <p style="text-align:center; font-size:15px; line-height:1.6;">
                    Confirmamos que tu correo de inicio de sesion en <strong>Kiadez</strong> fue actualizado correctamente.
                </p>

                <p style="text-align:center; font-size:14px; color:#555; margin:20px 0 0;">
                    Correo anterior: <strong>{previous_email}</strong><br />
                    Correo actual: <strong>{to_email}</strong>
                </p>

                <p style="text-align:center; font-size:14px; color:#555;">
                    Si no autorizaste este cambio, por favor contacta soporte de inmediato.
                </p>

                <hr style="border:none; border-top:1px solid #e0e0e0; margin:30px 0;">

                <p style="font-size:12px; color:#777; text-align:center;">
                    Kiadez · Ingenieria de la Conciencia<br>
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


def send_email_change_security_alert_email(*, to_email: str, new_email: str) -> None:
    subject = "Alerta de seguridad: cambio de correo en Kiadez"

    html_body = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
    <meta charset="UTF-8">
    <title>Alerta de seguridad · Kiadez</title>
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
                    Alerta de seguridad
                </h2>

                <p style="text-align:center; font-size:15px; line-height:1.6;">
                    Tu correo de inicio de sesion en <strong>Kiadez</strong> fue cambiado recientemente.
                </p>

                <p style="text-align:center; font-size:14px; color:#555; margin:20px 0 0;">
                    Nuevo correo configurado: <strong>{new_email}</strong>
                </p>

                <p style="text-align:center; font-size:14px; color:#555;">
                    Si no autorizaste este cambio, contacta soporte de inmediato.
                </p>

                <hr style="border:none; border-top:1px solid #e0e0e0; margin:30px 0;">

                <p style="font-size:12px; color:#777; text-align:center;">
                    Kiadez · Ingenieria de la Conciencia<br>
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


def send_minor_account_accreditation_email(
    *,
    to_email: str,
    minor_username: str,
    minor_email: str,
    registration_date_label: str,
    approval_url: str,
) -> None:
    subject = "Validación de cuenta de menor en Kiadez.com"

    safe_minor_username = html.escape(minor_username or "Usuario")
    safe_minor_email = html.escape(minor_email or "")
    safe_registration_date = html.escape(registration_date_label or "")
    safe_approval_url = html.escape(approval_url or "")

    html_body = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
    <meta charset="UTF-8">
    <title>Validación de cuenta de menor · Kiadez</title>
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
                    Estimado/a,
                </p>

                <p style="font-size:15px; line-height:1.7; margin:0 0 14px;">
                    Le informamos que el usuario <strong>{safe_minor_username}</strong>, asociado al correo
                    <strong>{safe_minor_email}</strong>, se registró en Kiadez.com el día
                    <strong>{safe_registration_date}</strong>.
                </p>

                <p style="font-size:15px; line-height:1.7; margin:0 0 14px;">
                    De acuerdo con la información suministrada durante el registro, el usuario es menor de edad,
                    por lo que su cuenta se encuentra actualmente en modo protegido.
                </p>

                <p style="font-size:15px; line-height:1.7; margin:0 0 14px;">
                    Esto significa que puede utilizar la plataforma, pero su contenido permanecerá privado y no será
                    visible públicamente hasta contar con la validación de un adulto responsable.
                </p>

                <p style="font-size:15px; line-height:1.7; margin:0 0 14px;">
                    Si usted autoriza que el menor bajo su responsabilidad pueda habilitar funciones públicas dentro
                    de la plataforma, puede aprobarlo haciendo clic en el siguiente enlace:
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
                    Aprobar validación
                    </a>
                </div>

                <p style="font-size:15px; line-height:1.7; margin:0 0 14px;">
                    En caso de no aprobar la habilitación pública, la cuenta continuará operando en modo privado.
                    También podrá gestionar ajustes adicionales de privacidad desde su panel correspondiente.
                </p>

                <p style="font-size:15px; line-height:1.7; margin:0 0 14px;">
                    Kiadez promueve el uso responsable y acompañado de la tecnología en menores de edad.
                </p>

                <p style="font-size:15px; line-height:1.7; margin:0;">
                    Atentamente,<br />
                    Equipo Kiadez
                </p>

                <p style="font-size:12px; line-height:1.6; color:#6b6b6b; margin:18px 0 0; word-break:break-all;">
                    Si el botón no funciona, copia y pega este enlace en tu navegador:<br />
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
