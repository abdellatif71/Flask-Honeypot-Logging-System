from flask import Flask, render_template, request, jsonify
import logging
from collections import Counter
ip_counter = Counter()

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

# Endpunkt zum Abrufen der Logs im JSON-Format
@app.route("/logs")
def logs():
    ip = request.remote_addr
    ip_counter[ip] += 1
    app.logger.info(f"IP {ip} hat {ip_counter[ip]} Anfragen gestellt.")
    try:
        # Lese die Logs aus der Datei
        with open("logs.txt", "r") as file:
            logs_data = file.readlines()
        
        # Struktur für das Log-Format, um sie als JSON zurückzugeben
        logs_json = []
        for log in logs_data:
            try:
                parts = log.split(" | ")
                ip = parts[0].replace("IP: ", "")
                user_agent = parts[1].replace("User-Agent: ", "")
                data = parts[2].replace("Data: ", "")
                logs_json.append({"IP": ip, "User-Agent": user_agent, "Data": data})
            except Exception as e:
                # Fehler beim Verarbeiten eines einzelnen Logs
                app.logger.error(f"Fehler beim Verarbeiten eines Logs: {str(e)}")
        
        # Rückgabe der Logs als JSON
        return jsonify(logs_json)
    
    except Exception as e:
        # Detailliertere Fehlerbeschreibung
        error_message = f"Fehler beim Abrufen der Logs: {str(e)}"
        app.logger.error(error_message)  # Protokolliere den Fehler
        return jsonify({"error": error_message}), 500



if __name__ == "__main__":
    print("Server läuft auf http://127.0.0.1:8080")
    app.run(debug=True, host="0.0.0.0", port=8080)


