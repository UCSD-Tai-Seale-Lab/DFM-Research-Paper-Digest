#!/usr/bin/env python3
"""
Email sender for publication reports
Supports sending HTML attachments or text summaries
"""

import os
import smtplib
import ssl
from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict, List


class EmailSender:
    """Send publication reports via email."""

    # Common SMTP configurations
    SMTP_CONFIGS = {
        "gmail": {"server": "smtp.gmail.com", "port": 587, "use_tls": True},
        "outlook": {"server": "smtp-mail.outlook.com", "port": 587, "use_tls": True},
        "yahoo": {"server": "smtp.mail.yahoo.com", "port": 587, "use_tls": True},
        "ucsd": {"server": "smtp.ucsd.edu", "port": 587, "use_tls": True},
    }

    def __init__(
        self,
        smtp_server: str = None,
        smtp_port: int = 587,
        use_tls: bool = True,
        provider: str = None,
    ):
        """
        Initialize email sender.

        Args:
            smtp_server: SMTP server address
            smtp_port: SMTP port (default: 587)
            use_tls: Use TLS encryption (default: True)
            provider: Email provider shortcut ('gmail', 'outlook', 'yahoo', 'ucsd')
        """
        if provider and provider.lower() in self.SMTP_CONFIGS:
            config = self.SMTP_CONFIGS[provider.lower()]
            self.smtp_server = config["server"]
            self.smtp_port = config["port"]
            self.use_tls = config["use_tls"]
        else:
            self.smtp_server = smtp_server or "smtp.gmail.com"
            self.smtp_port = smtp_port
            self.use_tls = use_tls

    def send_text_summary(
        self,
        publications: List[Dict],
        to_email: str,
        from_email: str,
        password: str,
        author_name: str,
        year: int,
        faculty_count: int = 0,
    ):
        """
        Send a text summary of publications via email (no attachment).

        Args:
            publications: List of publication dictionaries
            to_email: Recipient email address
            from_email: Sender email address
            password: Sender email password/app password
            author_name: Author name being queried
            year: Publication year
            faculty_count: Number of DFM faculty found
        """
        # Create message
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = f"Publications Report: {author_name} ({year})"

        # Build text body
        body = self._build_text_body(publications, author_name, year, faculty_count)
        msg.attach(MIMEText(body, "plain"))

        # Send email
        self._send_email(msg, from_email, to_email, password)

    def send_html_report(
        self,
        html_file: str,
        to_email: str,
        from_email: str,
        password: str,
        author_name: str,
        year: int,
    ):
        """
        Send HTML report as email attachment.

        Args:
            html_file: Path to HTML report file
            to_email: Recipient email address
            from_email: Sender email address
            password: Sender email password/app password
            author_name: Author name being queried
            year: Publication year
        """
        # Create message
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = f"Publications Report: {author_name} ({year})"

        # Email body
        body = f"""Hello,

Please find attached the publications report for {author_name} ({year}).

The report includes:
- Complete author lists for all publications
- DFM faculty members highlighted
- Publication dates and journal information
- Direct links to PubMed

Open the attached HTML file in your browser to view the formatted report.

Best regards
"""
        msg.attach(MIMEText(body, "plain"))

        # Attach HTML file
        try:
            with open(html_file, "rb") as f:
                attachment = MIMEBase("application", "octet-stream")
                attachment.set_payload(f.read())
                encoders.encode_base64(attachment)
                attachment.add_header(
                    "Content-Disposition",
                    f"attachment; filename={os.path.basename(html_file)}",
                )
                msg.attach(attachment)
        except FileNotFoundError:
            raise FileNotFoundError(f"HTML file not found: {html_file}")

        # Send email
        self._send_email(msg, from_email, to_email, password)

    def _build_text_body(
        self, publications: List[Dict], author_name: str, year: int, faculty_count: int
    ) -> str:
        """Build text email body with publication summary."""
        body = f"""Publications Report: {author_name} ({year})
{'='*80}

Summary:
  - Total Publications: {len(publications)}
  - DFM Faculty Co-authors: {faculty_count}

{'='*80}
Publications:
{'='*80}

"""

        for i, pub in enumerate(publications, 1):
            body += f"{i}. {pub['title']}\n\n"
            body += f"   Authors: {pub['authors']}\n"
            body += f"   Journal: {pub['journal']}\n"
            body += f"   Date: {pub.get('date', pub.get('year', 'N/A'))}\n"
            body += f"   PMID: {pub['pmid']}\n"
            body += f"   URL: https://pubmed.ncbi.nlm.nih.gov/{pub['pmid']}/\n\n"
            body += "-" * 80 + "\n\n"

        body += f"""
{'='*80}
Note: For a formatted report with DFM faculty highlighted, 
please request the HTML version.
{'='*80}
"""

        return body

    def _send_email(
        self, msg: MIMEMultipart, from_email: str, to_email: str, password: str
    ):
        """Send email via SMTP."""
        try:
            # Create secure SSL context
            context = ssl.create_default_context()

            # Connect to server
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls(context=context)

                # Login and send
                server.login(from_email, password)
                server.send_message(msg)

            print(f"\n✅ Email sent successfully to {to_email}")

        except smtplib.SMTPAuthenticationError:
            print("\n❌ Authentication failed. Check your email and password.")
            print("   For Gmail: Use an App Password (not your regular password)")
            print(
                "   Enable 2FA and create app password at: https://myaccount.google.com/apppasswords"
            )
        except smtplib.SMTPException as e:
            print(f"\n❌ SMTP error: {e}")
        except Exception as e:
            print(f"\n❌ Error sending email: {e}")


def main():
    """Test/demo function."""
    import argparse

    parser = argparse.ArgumentParser(description="Send publication report via email")
    parser.add_argument("--to", required=True, help="Recipient email")
    parser.add_argument("--from-email", required=True, help="Your email address")
    parser.add_argument(
        "--password", required=True, help="Your email password/app password"
    )
    parser.add_argument("--html-file", help="HTML report to attach")
    parser.add_argument(
        "--provider",
        choices=["gmail", "outlook", "yahoo", "ucsd"],
        default="gmail",
        help="Email provider",
    )

    args = parser.parse_args()

    sender = EmailSender(provider=args.provider)

    if args.html_file:
        sender.send_html_report(
            html_file=args.html_file,
            to_email=args.to,
            from_email=args.from_email,
            password=args.password,
            author_name="Test Author",
            year=datetime.now().year,
        )
    else:
        print("Please provide --html-file to send")


if __name__ == "__main__":
    main()
