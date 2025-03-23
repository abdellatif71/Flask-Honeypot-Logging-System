Flask Honeypot Logging System

This project is a simple Flask-based honeypot that logs potential attacks by capturing IP addresses, user agents, and any POST data sent to the server.

Requirements

Python 3

Flask (install using pip install flask)

How It Works

Captures Visitor Data:

Logs the IP address of the visitor.

Captures the User-Agent header.

Records any POST data sent to the server.

Logs Activity:

Stores the data in logs.txt.

Uses Python's built-in logging module for structured logging.

Installation & Setup

Clone this repository or download the script.

Install dependencies:

pip install flask

Run the application:

python app.py

Open a browser and go to http://127.0.0.1:5000/.

Code Overview

from flask import Flask, render_template, request
import logging

app = Flask(__name__)

# Configure logging (store attack attempts)
logging.basicConfig(filename="logs.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

@app.route("/", methods=["GET", "POST"])
def honeypot():
    ip = request.remote_addr
    user_agent = request.headers.get("User-Agent")
    
    # Extract POST data if available
    data = request.form if request.method == "POST" else "No POST data"
    
    # Log the request
    log_message = f"IP: {ip} | User-Agent: {user_agent} | Data: {data}"
    try:
        logging.info(log_message)
    except Exception as e:
        logging.error(f"Error logging request: {str(e)}")
    
    # Send log information to the HTML page
    return render_template("index.html", ip=ip, user_agent=user_agent, data=data)

if __name__ == "__main__":
    app.run(debug=True)

Features

Simple Logging: Captures request details and stores them in a log file.

Web Interface: Displays captured data in a user-friendly HTML template.

Error Handling: Catches and logs errors when writing to logs.txt.

Troubleshooting

If Flask is not installed, install it using pip install flask.

Ensure the logs.txt file has proper write permissions.

Disclaimer

This script is intended for educational and security research purposes only. Do not use it in unauthorized environments.

