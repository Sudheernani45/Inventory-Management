"""
Email utility – sends credentials via Flask-Mail.
Falls back to console print if mail is not configured.
"""
from flask import current_app

def send_credentials_email(to_email: str, name: str, password: str) -> bool:
    """
    Send login credentials to a new user.
    Returns True on success, False on failure.
    """
    try:
        from flask_mail import Message
        from extensions import mail

        msg = Message(
            subject="Your Inventory Management Credentials",
            recipients=[to_email],
            body=(
                f"Hello {name},\n\n"
                f"Your temporary password is: {password}\n\n"
                f"Please log in and change it immediately.\n\n"
                f"Regards,\nInventory Management"
            )
        )
        mail.send(msg)
        return True
    except Exception as e:
        # Fallback: print to console so credentials are not lost
        print(f"[EMAIL] To: {to_email}  Name: {name}  Temp Password: {password}  Error: {e}")
        return False
