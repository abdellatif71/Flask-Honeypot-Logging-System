from flask import Flask, render_template, request
import logging

app = Flask(__name__)

# Konfiguriere das Logging (Angriffe speichern)
logging.basicConfig(filename="logs.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

@app.route("/", methods=["GET", "POST"])
def honeypot():
    ip = request.remote_addr
    user_agent = request.headers.get("User-Agent")
    
    # Extrahiere POST-Daten, falls vorhanden
    data = request.form if request.method == "POST" else "Keine POST-Daten"
    
    # Protokolliere die Anfrage
    log_message = f"IP: {ip} | User-Agent: {user_agent} | Data: {data}"
    try:
        logging.info(log_message)
    except Exception as e:
        logging.error(f"Fehler beim Loggen der Anfrage: {str(e)}")
    
    # Sende Log-Informationen an die HTML-Seite
    return render_template("index.html", ip=ip, user_agent=user_agent, data=data)

if __name__ == "__main__":
    app.run(debug=True)
