from sqlite3 import connect
from turtle import home
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

app = Flask(__name__)

driver = None

USERNAME = "cpellerin"
PASSWORD = "corey"
LOGIN_URL = "http://10.0.7.2/login.aspx"

def init_browser():

    global driver
    
    if driver is not None:
        try:
            driver.title  # Check if browser is still open  
            return driver
        except:
            driver = None

    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    return driver

def login_to_site():
    global driver

    try:
        driver = init_browser()
        driver.get(LOGIN_URL)

        wait = WebDriverWait(driver, 10)

        # Username Entry
        username_field = wait.until(
            EC.presence_of_element_located((By.ID, "MainContent_UserName"))
        )
        username_field.clear()
        username_field.send_keys(USERNAME)

        # Password Entry
        password_field = wait.until(
            EC.presence_of_element_located((By.ID, "MainContent_Password"))
        )
        password_field.clear()
        password_field.send_keys(PASSWORD)

        # Connect button 
        login_button = wait.until(
            EC.element_to_be_clickable((By.ID, "MainContent_LoginButton"))
        )
        login_button.click()

        time.sleep(2)

        return True, "Login successful."

    except Exception as e:
        return False, f"Login failed: {str(e)}"


@app.route('/login', methods=['POST'])
def handle_login():
    success, message = login_to_site()

    return jsonify({
        "success": success,
        "message": message
        }), 200 if success else 500

@app.route('/input_barcode', methods=['POST'])
def handle_barcode():
    global driver

    data = request.json
    barcode = data.get('barcode', '')

    if not barcode:
        return jsonify({
            "success": False,
            "message": "No barcode provided."
        }), 400

    try:
        # If browser not open, login first
        if driver is None:
            success, message = login_to_site()
            if not success:
                return jsonify({"success": False, "message": message}), 500

        # Find the barcode input box
        wait = WebDriverWait(driver, 10)
        input_field = wait.until(
            EC.presence_of_element_located((By.NAME, "Barcode"))  # <-- adjust this
        )

        input_field.clear()
        input_field.send_keys(barcode)
        input_field.send_keys("\n")  # press Enter

        return jsonify({
            "success": True,
            "message": f"Barcode '{barcode}' sent successfully."
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error during barcode input: {str(e)}"
        }), 500


@app.route('/status', methods=['GET'])
def status():
    """Check if server is running"""
    return jsonify({
        'status': 'running',
        'browser_active': driver is not None
    }), 200

@app.route('/close', methods=['POST'])
def close_browser():
    """Close the browser"""
    global driver
    
    if driver:
        driver.quit()
        driver = None
        return jsonify({'message': 'Browser closed'}), 200
    
    return jsonify({'message': 'No browser to close'}), 200

if __name__ == '__main__':
    print("Starting automation server...")
    print(f"Server will run on: http://192.168.1.186:5000 (make sure to add /status)")
    print("\nAvailable endpoints:")
    print("  POST /login - Trigger login")
    print("  POST /input_barcode - Send barcode data")
    print("  GET  /status - Check server status")
    print("  POST /close - Close browser")
    
    # Run the server
    app.run(host='0.0.0.0', port=5000, debug=True)