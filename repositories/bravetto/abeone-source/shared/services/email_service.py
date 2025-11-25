"""
Email service implementation with DRY patterns.

This module provides a unified email service that can be used across the application
for sending emails through various providers (SendGrid, SES, SMTP, etc.).
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum

from pydantic import BaseModel, EmailStr, Field, validator


logger = logging.getLogger(__name__)


class EmailProvider(Enum):
    """Supported email service providers."""
    SENDGRID = "sendgrid"
    SES = "ses"
    SMTP = "smtp"
    CONSOLE = "console"  # For development/testing


class EmailTemplate(BaseModel):
    """Email template configuration."""
    name: str
    subject_template: str
    body_template: str
    html_template: Optional[str] = None

    @validator('subject_template', 'body_template')
    def validate_templates(cls, v):
        """Ensure templates use proper placeholder syntax."""
        if not isinstance(v, str):
            raise ValueError("Template must be a string")
        # Could add more validation for template syntax here
        return v


class EmailMessage(BaseModel):
    """Email message structure."""
    to_email: EmailStr
    subject: str
    body: str
    html_body: Optional[str] = None
    from_email: Optional[EmailStr] = None
    cc: Optional[List[EmailStr]] = None
    bcc: Optional[List[EmailStr]] = None
    reply_to: Optional[EmailStr] = None
    template_vars: Optional[Dict[str, Any]] = Field(default_factory=dict)
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class EmailConfig(BaseModel):
    """Email service configuration."""
    provider: EmailProvider = EmailProvider.CONSOLE
    api_key: Optional[str] = None
    smtp_host: Optional[str] = None
    smtp_port: Optional[int] = 587
    smtp_username: Optional[str] = None
    smtp_REPLACE_ME = None
    from_email: str = "noreply@aiguards.com"
    from_name: str = "AIGuards"
    rate_limit_per_minute: int = 100
    enable_tracking: bool = True


class EmailServiceError(Exception):
    """Base exception for email service errors."""
    pass


class EmailProviderError(EmailServiceError):
    """Error from email provider."""
    pass


class EmailRateLimitError(EmailServiceError):
    """Rate limit exceeded."""
    pass


class EmailProviderInterface(ABC):
    """Abstract base class for email providers."""

    def __init__(self, config: EmailConfig):
        self.config = config

    @abstractmethod
    async def send_email(self, message: EmailMessage) -> Dict[str, Any]:
        """Send an email message."""
        pass

    @abstractmethod
    async def validate_connection(self) -> bool:
        """Validate connection to email service."""
        pass


class SendGridProvider(EmailProviderInterface):
    """SendGrid email provider implementation."""

    async def send_email(self, message: EmailMessage) -> Dict[str, Any]:
        """Send email via SendGrid."""
        try:
            import sendgrid
            from sendgrid.helpers.mail import Mail, Email, To, Content

            if not self.config.api_key:
                raise EmailProviderError("SendGrid API key not configured")

            sg = sendgrid.SendGridAPIClient(api_key=self.config.api_key)

            from_email = Email(self.config.from_email, self.config.from_name)
            to_email = To(message.to_email)
            subject = message.subject

            # Use HTML if available, otherwise plain text
            content = Content(
                "text/html" if message.html_body else "text/plain",
                message.html_body or message.body
            )

            mail = Mail(from_email, to_email, subject, content)

            # Add CC/BCC if specified
            if message.cc:
                for cc_email in message.cc:
                    mail.add_cc(Email(cc_email))

            if message.bcc:
                for bcc_email in message.bcc:
                    mail.add_bcc(Email(bcc_email))

            response = sg.client.mail.send.post(request_body=mail.get())

            return {
                "provider": "sendgrid",
                "message_id": response.headers.get("X-Message-Id"),
                "status_code": response.status_code,
                "success": response.status_code == 202
            }

        except Exception as e:
            logger.error(f"SendGrid send error: {e}")
            raise EmailProviderError(f"SendGrid error: {str(e)}")

    async def validate_connection(self) -> bool:
        """Validate SendGrid connection."""
        try:
            import sendgrid
            sg = sendgrid.SendGridAPIClient(api_key=self.config.api_key)
            # Try to get account info
            response = sg.client.mail_settings.get()
            return response.status_code == 200
        except Exception as e:
            logger.error(f"SendGrid validation error: {e}")
            return False


class SESProvider(EmailProviderInterface):
    """AWS SES email provider implementation."""

    async def send_email(self, message: EmailMessage) -> Dict[str, Any]:
        """Send email via AWS SES."""
        try:
            import boto3
            from botocore.exceptions import BotoCoreError, ClientError

            ses_client = boto3.client('ses')

            email_data = {
                'Source': self.config.from_email,
                'Destination': {
                    'ToAddresses': [message.to_email],
                },
                'Message': {
                    'Subject': {
                        'Data': message.subject,
                    },
                    'Body': {
                        'Text': {
                            'Data': message.body,
                        }
                    }
                }
            }

            if message.html_body:
                email_data['Message']['Body']['Html'] = {
                    'Data': message.html_body
                }

            if message.cc:
                email_data['Destination']['CcAddresses'] = message.cc

            if message.bcc:
                email_data['Destination']['BccAddresses'] = message.bcc

            response = ses_client.send_email(**email_data)

            return {
                "provider": "ses",
                "message_id": response['MessageId'],
                "success": True
            }

        except (BotoCoreError, ClientError) as e:
            logger.error(f"SES send error: {e}")
            raise EmailProviderError(f"SES error: {str(e)}")

    async def validate_connection(self) -> bool:
        """Validate SES connection."""
        try:
            import boto3
            ses_client = boto3.client('ses')
            # Try to get send quota
            response = ses_client.get_send_quota()
            return 'Max24HourSend' in response
        except Exception as e:
            logger.error(f"SES validation error: {e}")
            return False


class SMTPProvider(EmailProviderInterface):
    """SMTP email provider implementation."""

    async def send_email(self, message: EmailMessage) -> Dict[str, Any]:
        """Send email via SMTP."""
        try:
            import aiosmtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart

            if not all([self.config.smtp_host, self.config.smtp_username, self.config.smtp_password]):
                raise EmailProviderError("SMTP configuration incomplete")

            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = message.subject
            msg['From'] = f"{self.config.from_name} <{self.config.from_email}>"
            msg['To'] = message.to_email

            if message.cc:
                msg['Cc'] = ', '.join(message.cc)
            if message.bcc:
                msg['Bcc'] = ', '.join(message.bcc)

            # Add body parts
            import email.mime.text
            text_part = email.mime.text.MIMEText(message.body, 'plain')
            msg.attach(text_part)

            if message.html_body:
                html_part = email.mime.text.MIMEText(message.html_body, 'html')
                msg.attach(html_part)

            # Send via SMTP
            await aiosmtplib.send(
                msg,
                hostname=self.config.smtp_host,
                port=self.config.smtp_port,
                username=self.config.smtp_username,
                REPLACE_ME
                use_tls=True
            )

            return {
                "provider": "smtp",
                "success": True
            }

        except Exception as e:
            logger.error(f"SMTP send error: {e}")
            raise EmailProviderError(f"SMTP error: {str(e)}")

    async def validate_connection(self) -> bool:
        """Validate SMTP connection."""
        try:
            import aiosmtplib
            await aiosmtplib.connect(
                hostname=self.config.smtp_host,
                port=self.config.smtp_port,
                username=self.config.smtp_username,
                REPLACE_ME
                use_tls=True
            )
            return True
        except Exception as e:
            logger.error(f"SMTP validation error: {e}")
            return False


class ConsoleProvider(EmailProviderInterface):
    """Console email provider for development/testing."""

    async def send_email(self, message: EmailMessage) -> Dict[str, Any]:
        """Log email to console instead of sending."""
        logger.info(f"EMAIL TO: {message.to_email}")
        logger.info(f"SUBJECT: {message.subject}")
        logger.info(f"BODY: {message.body}")
        if message.html_body:
            logger.info(f"HTML BODY: {message.html_body[:200]}...")

        return {
            "provider": "console",
            "message_id": f"console-{asyncio.get_event_loop().time()}",
            "success": True
        }

    async def validate_connection(self) -> bool:
        """Console provider always validates."""
        return True


class EmailService:
    """Unified email service with provider abstraction."""

    def __init__(self, config: EmailConfig):
        self.config = config
        self._provider = self._create_provider()
        self._rate_limiter = asyncio.Semaphore(config.rate_limit_per_minute)
        self._sent_emails = 0

    def _create_provider(self) -> EmailProviderInterface:
        """Create the appropriate email provider."""
        providers = {
            EmailProvider.SENDGRID: SendGridProvider,
            EmailProvider.SES: SESProvider,
            EmailProvider.SMTP: SMTPProvider,
            EmailProvider.CONSOLE: ConsoleProvider,
        }

        provider_class = providers.get(self.config.provider)
        if not provider_class:
            raise EmailServiceError(f"Unsupported email provider: {self.config.provider}")

        return provider_class(self.config)

    async def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        html_body: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Send an email message."""
        # Rate limiting
        await self._rate_limiter.acquire()

        try:
            message = EmailMessage(
                to_email=to_email,
                subject=subject,
                body=body,
                html_body=html_body,
                from_email=self.config.from_email,
                **kwargs
            )

            result = await self._provider.send_email(message)
            self._sent_emails += 1

            logger.info(f"Email sent successfully to {to_email} via {self.config.provider.value}")

            return result

        except EmailProviderError:
            raise
        except Exception as e:
            logger.error(f"Unexpected email error: {e}")
            raise EmailServiceError(f"Email service error: {str(e)}")
        finally:
            # Release rate limiter after a delay to enforce per-minute limit
            asyncio.create_task(self._release_rate_limiter())

    async def _release_rate_limiter(self):
        """Release rate limiter after delay."""
        await asyncio.sleep(60)  # 1 minute delay
        self._rate_limiter.release()

    async def send_template_email(
        self,
        template: EmailTemplate,
        to_email: str,
        template_vars: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Send an email using a template."""
        template_vars = template_vars or {}

        subject = template.subject_template.format(**template_vars)
        body = template.body_template.format(**template_vars)

        html_body = None
        if template.html_template:
            html_body = template.html_template.format(**template_vars)

        return await self.send_email(
            to_email=to_email,
            subject=subject,
            body=body,
            html_body=html_body,
            template_vars=template_vars,
            **kwargs
        )

    async def validate_connection(self) -> bool:
        """Validate connection to email service."""
        try:
            return await self._provider.validate_connection()
        except Exception as e:
            logger.error(f"Email connection validation failed: {e}")
            return False

    def get_stats(self) -> Dict[str, Any]:
        """Get email service statistics."""
        return {
            "provider": self.config.provider.value,
            "sent_emails": self._sent_emails,
            "rate_limit": self.config.rate_limit_per_minute,
            "connection_valid": None  # Would need async call
        }


# Global email service instance
_email_service: Optional[EmailService] = None


def get_email_service() -> EmailService:
    """Get the global email service instance."""
    global _email_service
    if _email_service is None:
        # Create default config - should be overridden by actual config
        config = EmailConfig()
        _email_service = EmailService(config)
    return _email_service


def init_email_service(config: EmailConfig) -> EmailService:
    """Initialize the global email service."""
    global _email_service
    _email_service = EmailService(config)
    return _email_service


# Convenience functions for common email operations
async def send_email(
    to_email: str,
    subject: str,
    body: str,
    html_body: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """Send an email using the global email service."""
    service = get_email_service()
    return await service.send_email(to_email, subject, body, html_body, **kwargs)


async def send_template_email(
    template: EmailTemplate,
    to_email: str,
    template_vars: Optional[Dict[str, Any]] = None,
    **kwargs
) -> Dict[str, Any]:
    """Send a template email using the global email service."""
    service = get_email_service()
    return await service.send_template_email(template, to_email, template_vars, **kwargs)
