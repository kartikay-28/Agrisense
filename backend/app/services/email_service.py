"""
Email service — sends weekly insight emails via SMTP.
Configure SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD in .env
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")


def send_weekly_insight(
    to_email: str,
    farmer_name: str,
    farm_name: str,
    recommendations: list[dict],
    weather_summary: str,
) -> bool:
    """
    Send a weekly HTML insight email to a farmer.

    Parameters:
    -----------
    to_email : str
    farmer_name : str
    farm_name : str
    recommendations : list of {crop, match_score, expected_price, reason}
    weather_summary : str  — e.g. "Heavy rains expected next week"

    Returns True on success, False on failure.
    """
    if not SMTP_USER:
        print(f"[email_service] SMTP not configured — skipping email to {to_email}")
        return False

    subject = f"AgriSense Weekly Insight — {farm_name}"

    # Build recommendation rows
    rows = "".join(
        f"<tr><td>{r['crop']}</td><td>{r['match_score']}</td>"
        f"<td>{r['expected_price']}</td><td>{r['reason']}</td></tr>"
        for r in recommendations
    )

    html = f"""
    <html><body style="font-family:sans-serif;color:#2C2416;background:#F5F1EA;padding:24px;">
      <h2 style="color:#5C7A52;">AgriSense Weekly Insight</h2>
      <p>Hello <strong>{farmer_name}</strong>,</p>
      <p>{weather_summary} at <strong>{farm_name}</strong>.</p>
      <h3>Top Crop Recommendations This Week</h3>
      <table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse;width:100%;">
        <thead style="background:#DDE8D9;">
          <tr><th>Crop</th><th>Match Score</th><th>Expected Price</th><th>Reason</th></tr>
        </thead>
        <tbody>{rows}</tbody>
      </table>
      <p style="margin-top:24px;font-size:12px;color:#7A6A55;">
        Powered by AgriSense ML · Unsubscribe anytime from your profile.
      </p>
    </body></html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = to_email
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, to_email, msg.as_string())
        print(f"[email_service] Sent weekly insight to {to_email}")
        return True
    except Exception as e:
        print(f"[email_service] Failed to send email: {e}")
        return False
