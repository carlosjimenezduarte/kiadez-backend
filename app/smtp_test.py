
import smtplib
from email.message import EmailMessage

SMTP_HOST = "smtp.hostinger.com"
SMTP_PORT = 465  # SSL
SMTP_USER = "noreply@kiadez.com"
SMTP_PASS = "ProyectoLibertad2026++"

msg = EmailMessage()
msg["From"] = SMTP_USER
msg["To"] = "melqui7des@gmail.com"
msg["Subject"] = "Prueba SMTP Kiadez"
msg.set_content("Si lees esto, el SMTP de Kiadez funciona correctamente 🚀")

print("🔌 Conectando a Hostinger SMTP (SSL)...")

with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
    server.login(SMTP_USER, SMTP_PASS)
    server.send_message(msg)

print("Email sent successfully")
