import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.core.config import settings


def send_verification_email(to_email: str, token: str):
    verify_url = f"http://localhost:8000/auth/verify-email?token={token}"


    subject = "Verifica tu correo electrónico en Kiadez"

    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>Bienvenido a Kiadez</h2>
            <p>Gracias por registrarte.</p>
            <p>Para activar tu cuenta, haz clic en el siguiente enlace:</p>
            <p>
                <a href="{verify_url}"
                   style="display:inline-block;padding:10px 15px;
                          background-color:#00674F;color:#fff;
                          text-decoration:none;border-radius:4px;">
                    Verificar correo
                </a>
            </p>
            <p>Si no solicitaste esta cuenta, puedes ignorar este mensaje.</p>
            <hr>
            <small>Kiadez · Ingeniería de la Conciencia</small>
        </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["From"] = settings.SMTP_FROM
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)
