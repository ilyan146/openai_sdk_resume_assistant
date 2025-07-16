import os
from typing import Dict

import sendgrid  # type: ignore
from dotenv import load_dotenv
from sendgrid.helpers.mail import Content, Email, Mail, To  # type: ignore

load_dotenv(override=True)


def send_email(subject: str, body: str) -> Dict[str, str]:
    sg = sendgrid.SendGridAPIClient(api_key=os.getenv("SENDGRID_API_KEY"))
    from_email = Email("mohamed.ilyan@boskalis.com")
    to_email = To("ilyan146@gmail.com")
    content = Content("text/plain", body)
    mail = Mail(from_email, to_email, subject, content).get()
    response = sg.client.mail.send.post(request_body=mail)
    print("Email response", response.status_code)

    return {"status": "success"}
