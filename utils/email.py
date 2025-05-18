"""
Email utilities for sending OTP emails.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

from config.settings import EMAIL_CONFIG

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_otp_email(recipient_email: str, otp: str):
    """
    Send an OTP email to the user for password reset.
    
    Args:
        recipient_email: The email address of the recipient.
        otp: The OTP to be sent.
    
    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    # Extract email configuration
    sender_email = EMAIL_CONFIG["email"]
    sender_password = EMAIL_CONFIG["password"]
    
    # Check if email credentials are configured
    if not sender_email or not sender_password:
        logger.error("Email credentials not configured. Please update settings.py")
        return False
    
    # Create email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = "Password Reset OTP - Todo App"
    
    # Email body
    body = f"""
    <html>
    <body>
        <h2>Password Reset Request</h2>
        <p>Hello,</p>
        <p>We received a request to reset your password for the Todo App. Here is your One Time Password (OTP):</p>
        <h3 style="background-color: #f2f2f2; padding: 10px; font-size: 24px; letter-spacing: 5px; text-align: center;">{otp}</h3>
        <p>This OTP will expire in 15 minutes. If you did not request a password reset, please ignore this email.</p>
        <p>Thank you,<br>Todo App Team</p>
    </body>
    </html>
    """
    
    # Attach body to the message
    message.attach(MIMEText(body, "html"))
    
    try:
        # Connect to the SMTP server
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            # Login to the email account
            server.login(sender_email, sender_password)
            
            # Send the email
            server.send_message(message)
            
        logger.info(f"OTP email sent successfully to {recipient_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send OTP email: {str(e)}")
        return False
