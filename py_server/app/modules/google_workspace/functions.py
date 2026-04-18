from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from uuid import uuid4

from google.oauth2 import service_account
from googleapiclient.discovery import build

from app.core.config import settings


CALENDAR_SCOPES = ["https://www.googleapis.com/auth/calendar"]


def send_email_smtp(
    to_emails: list[str] | str,
    subject: str,
    body_text: str,
    body_html: str | None = None,
    cc: list[str] | None = None,
    bcc: list[str] | None = None,
) -> dict:
    if isinstance(to_emails, str):
        recipients = [to_emails]
    else:
        recipients = to_emails

    if not settings.smtp_host or not settings.smtp_username or not settings.smtp_password:
        raise RuntimeError("SMTP is not configured. Set SMTP_HOST, SMTP_USERNAME, SMTP_PASSWORD.")

    sender = settings.smtp_from_email or settings.smtp_username
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = ", ".join(recipients)
    if cc:
        message["Cc"] = ", ".join(cc)

    message.attach(MIMEText(body_text, "plain"))
    if body_html:
        message.attach(MIMEText(body_html, "html"))

    all_recipients = recipients + (cc or []) + (bcc or [])

    if settings.smtp_use_ssl:
        with smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port) as smtp:
            smtp.login(settings.smtp_username, settings.smtp_password)
            smtp.sendmail(sender, all_recipients, message.as_string())
    else:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as smtp:
            if settings.smtp_use_tls:
                smtp.starttls()
            smtp.login(settings.smtp_username, settings.smtp_password)
            smtp.sendmail(sender, all_recipients, message.as_string())

    return {
        "status": "sent",
        "to": recipients,
        "cc": cc or [],
        "bcc": bcc or [],
        "subject": subject,
    }


def _calendar_service():
    if not settings.google_service_account_file:
        raise RuntimeError("GOOGLE_SERVICE_ACCOUNT_FILE is not configured")

    credentials = service_account.Credentials.from_service_account_file(
        settings.google_service_account_file,
        scopes=CALENDAR_SCOPES,
    )

    if settings.google_workspace_delegated_user:
        credentials = credentials.with_subject(settings.google_workspace_delegated_user)

    return build("calendar", "v3", credentials=credentials)


def create_calendar_event(
    summary: str,
    start_iso: str,
    end_iso: str,
    timezone: str = "UTC",
    description: str | None = None,
    attendees: list[str] | None = None,
    location: str | None = None,
    calendar_id: str | None = None,
) -> dict:
    service = _calendar_service()
    event = {
        "summary": summary,
        "description": description or "",
        "location": location or "",
        "start": {"dateTime": start_iso, "timeZone": timezone},
        "end": {"dateTime": end_iso, "timeZone": timezone},
        "attendees": [{"email": email} for email in (attendees or [])],
    }

    target_calendar = calendar_id or settings.google_calendar_id
    created = (
        service.events()
        .insert(calendarId=target_calendar, body=event, sendUpdates="all")
        .execute()
    )

    return {
        "id": created.get("id"),
        "html_link": created.get("htmlLink"),
        "hangout_link": created.get("hangoutLink"),
        "status": created.get("status"),
    }


def schedule_google_meet(
    summary: str,
    start_iso: str,
    end_iso: str,
    timezone: str = "UTC",
    description: str | None = None,
    attendees: list[str] | None = None,
    calendar_id: str | None = None,
) -> dict:
    service = _calendar_service()
    event = {
        "summary": summary,
        "description": description or "",
        "start": {"dateTime": start_iso, "timeZone": timezone},
        "end": {"dateTime": end_iso, "timeZone": timezone},
        "attendees": [{"email": email} for email in (attendees or [])],
        "conferenceData": {
            "createRequest": {
                "requestId": f"meet-{uuid4()}",
                "conferenceSolutionKey": {"type": "hangoutsMeet"},
            }
        },
    }

    target_calendar = calendar_id or settings.google_calendar_id
    created = (
        service.events()
        .insert(
            calendarId=target_calendar,
            body=event,
            conferenceDataVersion=1,
            sendUpdates="all",
        )
        .execute()
    )

    return {
        "id": created.get("id"),
        "html_link": created.get("htmlLink"),
        "meet_link": created.get("hangoutLink"),
        "status": created.get("status"),
        "start": created.get("start", {}).get("dateTime"),
        "end": created.get("end", {}).get("dateTime"),
    }
