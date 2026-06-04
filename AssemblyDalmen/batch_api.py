import pyodbc
from flask import Flask, jsonify
import re

app = Flask(__name__)

CONNECTION_STRING = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=10.0.7.2,1433;"
    "DATABASE=BDSuiviProd;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

def parse_scan(scanned: str):
    parts = scanned.strip().split('-')
    if len(parts) != 4:
        return None
    commande_id = f"{parts[0]}-{parts[1]}"
    produit_id = parts[2]
    quantite_id = parts[3]
    return commande_id, produit_id, quantite_id

@app.route('/batch/<path:scan_code>')
def get_batch(scan_code: str):
    parsed = parse_scan(scan_code)
    if not parsed:
        return jsonify({"error": "Invalid scan format"}), 400

    commande_id, produit_id, quantite_id = parsed
    produit_alt = produit_id.lstrip('0') or '0'

    query = """
        SELECT TOP 1 [BatchNO]
        FROM [dbo].[CODEBAR]
        WHERE [CommandeID] = ?
          AND [ProduitID] IN (?, ?)
          AND [QuantiteID] = ?
    """

    try:
        conn = pyodbc.connect(CONNECTION_STRING, timeout=5)
        cursor = conn.cursor()
        cursor.execute(query, commande_id, produit_id, produit_alt, quantite_id)
        row = cursor.fetchone()
        conn.close()

        if row:
            return jsonify({"BatchNO": str(row[0])})
        else:
            return jsonify({"BatchNO": None}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)