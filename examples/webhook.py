import os, requests

def send_webhook_message(webhook_url, text):
    data = {"content": text}
    requests.post(webhook_url, json=data)

def on_poll_update(monitor):
    send_webhook_message(os.getenv('MATHMATIZE_WEBHOOK_URL'), 'my text')