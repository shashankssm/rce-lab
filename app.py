from flask import Flask, request, render_template_string
import subprocess
import pytz
from datetime import datetime, timezone

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
    <!doctype html>
    <html>
    <head>
        <title>Timezone Fetcher</title>
        <style>
            body {
                background: linear-gradient(to right, #ff7e5f, #feb47b);
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 50px;
            }
            button {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
            }
            .response {
                background-color: white;
                padding: 20px;
                border-radius: 10px;
                display: inline-block;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <h1>Fetch Current Time for All Timezones</h1>
        <form method="post" action="/fetch-time" id="fetchForm">
            <button type="button" onclick="fetchTime()">Fetch Time</button>
        </form>
        <div id="response" class="response"></div>
        <script>
            function fetchTime() {
                fetch('/fetch-time', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: 'cmd=date'
                })
                .then(response => response.text())
                .then(data => {
                    document.getElementById('response').innerHTML = data;
                });
            }
        </script>
    </body>
    </html>
    ''')

@app.route('/fetch-time', methods=['POST'])
def fetch_time():
    cmd = request.form.get('cmd')
    # Directly execute the command without validation
    output = subprocess.check_output(cmd, shell=True).decode()
    times = ""
    for tz in pytz.all_timezones:
        times += f"{tz}: {datetime.now(pytz.timezone(tz)).strftime('%Y-%m-%d %H:%M:%S')}<br>"
    return f"<pre>{output}\n\n{times}</pre>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)

