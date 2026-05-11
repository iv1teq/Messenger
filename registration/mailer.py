import smtplib
import email.message as msg
from config import APP_PASSWORD

def send_email(user_email):
    with smtplib.SMTP(host = "smtp.gmail.com", port = 587) as smtp:
        smtp.starttls()
        smtp.login(
            user ="worldit.messeger@gmail.com",
            password= APP_PASSWORD
            )
        email_msg = msg.EmailMessage()
        email_msg["Subject"] = "TEST"
        email_msg["From"] = "worldit.messeger@gmail.com"
        email_msg["To"] = user_email
        
        html = f"""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                <meta charset="UTF-8">

                <style>

                    body{{
                        margin:0;
                        padding:40px 15px;
                        background:#f4f6fb;
                        font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif;
                    }}

                    .container{{
                        max-width:600px;
                        margin:0 auto;
                        background:white;
                        padding:50px 40px;
                        border-radius:24px;
                        border:1px solid #dbe1ea;
                        text-align:center;
                        box-shadow:0 10px 25px rgba(0,0,0,0.05);
                    }}

                    h1{{
                        margin:0 0 18px;
                        font-size:32px;
                        color:#111827;
                    }}

                    p{{
                        margin:0 0 35px;
                        color:#6b7280;
                        font-size:16px;
                        line-height:1.7;
                    }}

                    .confirm-btn{{
                        display:block;
                        width:100%;
                        padding:15px 0;
                        background:#2aabee;
                        color:white !important;
                        text-decoration:none;
                        border-radius:14px;
                        font-size:16px;
                        font-weight:600;
                        box-sizing:border-box;
                    }}

                    .confirm-btn:hover{{
                        background:#1f9cdd;
                    }}

                    hr{{
                        border:none;
                        border-top:1px solid #e5e7eb;
                        margin:40px 0 30px;
                    }}

                    .bottom-text{{
                        font-size:14px;
                        color:#9ca3af;
                        line-height:1.7;
                    }}

                </style>
                </head>

                <body>

                    <div class="container">

                        <h1>
                            Welcome to WorldIT Messenger
                        </h1>

                        <p>
                            Press the button below to confirm your email address
                            and complete your registration.
                        </p>

                        <a href="http://127.0.0.1:5000/email_confirmation?email={user_email}" class="confirm-btn">
                            Confirm Email
                        </a>

                        <hr>

                        <div class="bottom-text">
                            If you have any questions — we are always happy to help.
                            <br><br>

                            Best wishes,<br>
                            World IT Academy Team
                        </div>

                    </div>

                </body>
                </html>
                """
        email_msg.add_alternative(
            html,
            subtype = "html"
        )
        smtp.send_message(email_msg)