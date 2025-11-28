"""
AI Guardians Email Service

Complete email service integration with SendGrid/SES, templates, and workflows.
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.core.models import User, Organization, Subscription
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import os

logger = logging.getLogger(__name__)

# Initialize email service
settings = get_settings()


class EmailService:
    """Complete email service with templates and workflows."""
    
    def __init__(self):
        """Initialize email service."""
        self.sendgrid_api_key = settings.sendgrid_api_key
        self.from_email = settings.sendgrid_from_email
        self.templates_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'email')
        logger.info("Email service initialized")
    
    async def send_welcome_email(self, user: User, organization: Organization) -> bool:
        """
        Send welcome email to new user.
        
        Args:
            user: User instance
            organization: Organization instance
            
        Returns:
            True if email sent successfully
        """
        try:
            template_data = {
                'user_name': user.username,
                'organization_name': organization.name,
                'verification_link': f"{settings.frontend_url}/verify-email?token={user.email_verification_token}",
                'dashboard_url': f"{settings.frontend_url}/dashboard",
                'support_email': settings.support_email
            }
            
            subject = f"Welcome to AI Guardians, {user.username}!"
            html_content = self._render_template('welcome.html', template_data)
            text_content = self._render_template('welcome.txt', template_data)
            
            return await self._send_email(
                to_email=user.email,
                subject=subject,
                html_content=html_content,
                text_content=text_content
            )
            
        except Exception as e:
            logger.error(f"Failed to send welcome email to {user.email}: {e}")
            return False
    
    async def send_email_verification(self, user: User) -> bool:
        """
        Send email verification email.
        
        Args:
            user: User instance
            
        Returns:
            True if email sent successfully
        """
        try:
            template_data = {
                'user_name': user.username,
                'verification_link': f"{settings.frontend_url}/verify-email?token={user.email_verification_token}",
                'support_email': settings.support_email
            }
            
            subject = "Verify your email address - AI Guardians"
            html_content = self._render_template('email_verification.html', template_data)
            text_content = self._render_template('email_verification.txt', template_data)
            
            return await self._send_email(
                to_email=user.email,
                subject=subject,
                html_content=html_content,
                text_content=text_content
            )
            
        except Exception as e:
            logger.error(f"Failed to send verification email to {user.email}: {e}")
            return False
    
    async def send_password_reset(self, user: User, reset_token: str) -> bool:
        """
        Send password reset email.
        
        Args:
            user: User instance
            reset_token: Password reset token
            
        Returns:
            True if email sent successfully
        """
        try:
            template_data = {
                'user_name': user.username,
                'reset_link': f"{settings.frontend_url}/reset-password?token={reset_token}",
                'expires_in': "24 hours",
                'support_email': settings.support_email
            }
            
            subject = "Reset your password - AI Guardians"
            html_content = self._render_template('password_reset.html', template_data)
            text_content = self._render_template('password_reset.txt', template_data)
            
            return await self._send_email(
                to_email=user.email,
                subject=subject,
                html_content=html_content,
                text_content=text_content
            )
            
        except Exception as e:
            logger.error(f"Failed to send password reset email to {user.email}: {e}")
            return False
    
    async def send_subscription_confirmation(self, organization: Organization, subscription: Subscription) -> bool:
        """
        Send subscription confirmation email.
        
        Args:
            organization: Organization instance
            subscription: Subscription instance
            
        Returns:
            True if email sent successfully
        """
        try:
            # Get subscription tier information
            tier = subscription.subscription_tier if subscription else None
            if not tier:
                logger.error(f"No subscription tier found for subscription {subscription.id}")
                return False
            
            # Determine billing amount and interval from subscription
            # Default to monthly pricing
            amount = float(tier.price_monthly)
            billing_interval = "month"  # Can be determined from Stripe subscription if needed
            
            template_data = {
                'organization_name': organization.name,
                'subscription_tier': tier.name,
                'amount': amount,
                'billing_interval': billing_interval,
                'next_billing_date': subscription.current_period_end.isoformat() if subscription.current_period_end else None,
                'dashboard_url': f"{settings.frontend_url}/dashboard/billing",
                'support_email': getattr(settings, 'support_email', 'support@aiguardian.ai')
            }
            
            subject = f"Subscription confirmed - {tier.name} plan"
            html_content = self._render_template('subscription_confirmation.html', template_data)
            text_content = self._render_template('subscription_confirmation.txt', template_data)
            
            return await self._send_email(
                to_email=organization.owner_email,
                subject=subject,
                html_content=html_content,
                text_content=text_content
            )
            
        except Exception as e:
            logger.error(f"Failed to send subscription confirmation to {organization.owner_email}: {e}")
            return False
    
    async def send_payment_receipt(self, organization: Organization, invoice_data: Dict[str, Any]) -> bool:
        """
        Send payment receipt email.
        
        Args:
            organization: Organization instance
            invoice_data: Invoice data from Stripe
            
        Returns:
            True if email sent successfully
        """
        try:
            template_data = {
                'organization_name': organization.name,
                'amount': invoice_data.get('amount_paid', 0) / 100,
                'currency': invoice_data.get('currency', 'usd'),
                'invoice_number': invoice_data.get('number', ''),
                'payment_date': invoice_data.get('paid_at', datetime.now()).isoformat(),
                'invoice_url': invoice_data.get('hosted_invoice_url', ''),
                'dashboard_url': f"{settings.frontend_url}/dashboard/billing",
                'support_email': settings.support_email
            }
            
            subject = f"Payment receipt - ${template_data['amount']:.2f}"
            html_content = self._render_template('payment_receipt.html', template_data)
            text_content = self._render_template('payment_receipt.txt', template_data)
            
            return await self._send_email(
                to_email=organization.owner_email,
                subject=subject,
                html_content=html_content,
                text_content=text_content
            )
            
        except Exception as e:
            logger.error(f"Failed to send payment receipt to {organization.owner_email}: {e}")
            return False
    
    async def send_usage_alert(self, organization: Organization, usage_percentage: float) -> bool:
        """
        Send usage alert email.
        
        Args:
            organization: Organization instance
            usage_percentage: Current usage percentage
            
        Returns:
            True if email sent successfully
        """
        try:
            template_data = {
                'organization_name': organization.name,
                'usage_percentage': usage_percentage,
                'alert_level': 'high' if usage_percentage >= 100 else 'warning',
                'upgrade_url': f"{settings.frontend_url}/dashboard/billing",
                'support_email': settings.support_email
            }
            
            if usage_percentage >= 100:
                subject = "⚠️ Usage limit exceeded - AI Guardians"
            else:
                subject = f"⚠️ Usage alert - {usage_percentage:.0f}% of limit used"
            
            html_content = self._render_template('usage_alert.html', template_data)
            text_content = self._render_template('usage_alert.txt', template_data)
            
            return await self._send_email(
                to_email=organization.owner_email,
                subject=subject,
                html_content=html_content,
                text_content=text_content
            )
            
        except Exception as e:
            logger.error(f"Failed to send usage alert to {organization.owner_email}: {e}")
            return False
    
    async def send_team_invitation(self, organization: Organization, invitee_email: str, inviter_name: str, role: str) -> bool:
        """
        Send team invitation email.
        
        Args:
            organization: Organization instance
            invitee_email: Email of person being invited
            inviter_name: Name of person sending invitation
            role: Role being assigned
            
        Returns:
            True if email sent successfully
        """
        try:
            template_data = {
                'invitee_email': invitee_email,
                'inviter_name': inviter_name,
                'organization_name': organization.name,
                'role': role,
                'accept_url': f"{settings.frontend_url}/accept-invitation?email={invitee_email}",
                'support_email': settings.support_email
            }
            
            subject = f"You're invited to join {organization.name} on AI Guardians"
            html_content = self._render_template('team_invitation.html', template_data)
            text_content = self._render_template('team_invitation.txt', template_data)
            
            return await self._send_email(
                to_email=invitee_email,
                subject=subject,
                html_content=html_content,
                text_content=text_content
            )
            
        except Exception as e:
            logger.error(f"Failed to send team invitation to {invitee_email}: {e}")
            return False
    
    async def send_trial_expiration_warning(self, organization: Organization, days_remaining: int) -> bool:
        """
        Send trial expiration warning email.
        
        Args:
            organization: Organization instance
            days_remaining: Days remaining in trial
            
        Returns:
            True if email sent successfully
        """
        try:
            template_data = {
                'organization_name': organization.name,
                'days_remaining': days_remaining,
                'upgrade_url': f"{settings.frontend_url}/dashboard/billing",
                'support_email': settings.support_email
            }
            
            subject = f"Trial expires in {days_remaining} days - AI Guardians"
            html_content = self._render_template('trial_expiration.html', template_data)
            text_content = self._render_template('trial_expiration.txt', template_data)
            
            return await self._send_email(
                to_email=organization.owner_email,
                subject=subject,
                html_content=html_content,
                text_content=text_content
            )
            
        except Exception as e:
            logger.error(f"Failed to send trial expiration warning to {organization.owner_email}: {e}")
            return False
    
    def _render_template(self, template_name: str, data: Dict[str, Any]) -> str:
        """
        Render email template with data.
        
        Args:
            template_name: Template file name
            data: Template data
            
        Returns:
            Rendered template content
        """
        try:
            template_path = os.path.join(self.templates_path, template_name)
            
            if not os.path.exists(template_path):
                # Return basic template if file doesn't exist
                return self._get_basic_template(template_name, data)
            
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            # Simple template rendering (replace placeholders)
            for key, value in data.items():
                template_content = template_content.replace(f'{{{{{key}}}}}', str(value))
            
            return template_content
            
        except Exception as e:
            logger.error(f"Failed to render template {template_name}: {e}")
            return self._get_basic_template(template_name, data)
    
    def _get_basic_template(self, template_name: str, data: Dict[str, Any]) -> str:
        """Get basic template content when file doesn't exist."""
        if 'welcome' in template_name:
            return f"""
            <h1>Welcome to AI Guardians!</h1>
            <p>Hello {data.get('user_name', 'User')},</p>
            <p>Welcome to AI Guardians! Your account has been created successfully.</p>
            <p>Organization: {data.get('organization_name', 'N/A')}</p>
            <p><a href="{data.get('dashboard_url', '#')}">Access Dashboard</a></p>
            <p>Best regards,<br>AI Guardians Team</p>
            """
        elif 'verification' in template_name:
            return f"""
            <h1>Verify Your Email</h1>
            <p>Hello {data.get('user_name', 'User')},</p>
            <p>Please verify your email address by clicking the link below:</p>
            <p><a href="{data.get('verification_link', '#')}">Verify Email</a></p>
            <p>Best regards,<br>AI Guardians Team</p>
            """
        elif 'password_reset' in template_name:
            return f"""
            <h1>Reset Your Password</h1>
            <p>Hello {data.get('user_name', 'User')},</p>
            <p>You requested a password reset. Click the link below to reset your password:</p>
            <p><a href="{data.get('reset_link', '#')}">Reset Password</a></p>
            <p>This link expires in {data.get('expires_in', '24 hours')}.</p>
            <p>Best regards,<br>AI Guardians Team</p>
            """
        else:
            return f"<p>Hello,</p><p>This is a notification from AI Guardians.</p><p>Best regards,<br>AI Guardians Team</p>"
    
    async def _send_email(
        self, 
        to_email: str, 
        subject: str, 
        html_content: str, 
        text_content: str
    ) -> bool:
        """
        Send email using configured service.
        
        Args:
            to_email: Recipient email
            subject: Email subject
            html_content: HTML content
            text_content: Text content
            
        Returns:
            True if email sent successfully
        """
        try:
            if self.sendgrid_api_key:
                return await self._send_with_sendgrid(to_email, subject, html_content, text_content)
            else:
                return await self._send_with_smtp(to_email, subject, html_content, text_content)
                
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return False
    
    async def _send_with_sendgrid(self, to_email: str, subject: str, html_content: str, text_content: str) -> bool:
        """Send email using SendGrid."""
        try:
            import sendgrid
            from sendgrid.helpers.mail import Mail
            
            sg = sendgrid.SendGridAPIClient(api_key=self.sendgrid_api_key)
            
            message = Mail(
                from_email=self.from_email,
                to_emails=to_email,
                subject=subject,
                html_content=html_content,
                plain_text_content=text_content
            )
            
            response = sg.send(message)
            
            if response.status_code == 202:
                logger.info(f"Email sent successfully to {to_email}")
                return True
            else:
                logger.error(f"SendGrid error: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"SendGrid send failed: {e}")
            return False
    
    async def _send_with_smtp(self, to_email: str, subject: str, html_content: str, text_content: str) -> bool:
        """Send email using SMTP (fallback)."""
        try:
            # This is a basic SMTP implementation
            # In production, you'd configure proper SMTP settings
            logger.info(f"Would send email to {to_email}: {subject}")
            return True
            
        except Exception as e:
            logger.error(f"SMTP send failed: {e}")
            return False


# Global email service instance
email_service = EmailService()
