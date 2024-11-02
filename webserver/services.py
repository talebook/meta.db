#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def send_email(email, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'your_email@example.com'
    msg['To'] = email

    s = smtplib.SMTP('smtp.example.com')
    s.sendmail('your_email@example.com', [email], msg.as_string())
    s.quit()
