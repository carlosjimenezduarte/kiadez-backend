from __future__ import annotations

import argparse

from app.core.config import settings
from app.core.mailer import send_html_email


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Send a local test email using configured provider (smtp or mailgun)."
    )
    parser.add_argument("--to", required=True, help="Destination email address.")
    parser.add_argument(
        "--subject",
        default="Prueba de correo Kiadez",
        help="Email subject.",
    )
    parser.add_argument(
        "--message",
        default="Si lees este correo, el proveedor configurado funciona correctamente.",
        help="Plain message content.",
    )
    args = parser.parse_args()

    html_body = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <title>{args.subject}</title>
    </head>
    <body style="font-family: Arial, Helvetica, sans-serif; color:#1e1e1e;">
      <h2>Prueba de proveedor de correo</h2>
      <p>{args.message}</p>
      <p><strong>Proveedor:</strong> {settings.EMAIL_PROVIDER}</p>
    </body>
    </html>
    """

    send_html_email(
        to_email=args.to.strip(),
        subject=args.subject.strip(),
        html_body=html_body,
    )

    print(f"Email sent successfully via provider={settings.EMAIL_PROVIDER!r} to {args.to!r}.")


if __name__ == "__main__":
    main()
