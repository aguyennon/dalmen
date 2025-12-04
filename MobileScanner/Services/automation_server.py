from re import A
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

driver = None

USERNAME = "cpellerin"
PASSWORD = "corey"
LOGIN_URL = "http://10.0.7.2/login.aspx"
STOCKTAKING_URL = "http://10.0.7.2/StockTaking.aspx"

def init_browser():
    global driver

    if driver is not None:
        try:
            driver.title
            logger.info("Browser already initialized and active")
            return driver
        except:
            logger.warning("Browser was initialized but became inactive, reinitializing...")
            driver = None

    logger.info("Initializing new browser instance...")
    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()
        logger.info("Browser initialized successfully")
        return driver
    except Exception as e:
        logger.error(f"Failed to initialize browser: {e}")
        raise


def get_driver():
    return init_browser()

def is_logged_in():
    global driver

    if driver is None:
        logger.info("Browser not initialized, user not logged in")
        return False

    try:
        current_url = driver.current_url
        logger.info(f"Checking login status. Current URL: {current_url}")

        # Handle blank page
        if current_url == "data:," or not current_url.startswith("http"):
            logger.info("On blank page (data:,) - not logged in")
            return False

        if "StockTaking.aspx" in current_url or "login.aspx" not in current_url.lower():

            try:
                wait = WebDriverWait(driver, 2)
                wait.until(EC.presence_of_element_located((By.ID, "MainContent_txtNumberScan")))
                logger.info("Already logged in and on StockTaking page")
                return True
            except:
                logger.info("On authenticated page but StockTaking elements not found")
                return False

        logger.info("Not logged in - on login page or other page")
        return False

    except Exception as e:
        logger.error(f"Error checking login status: {e}")
        return False

def ensure_on_stocktaking_page():
    global driver
    driver = get_driver()

    current_url = driver.current_url
    logger.info(f"Current URL: {current_url}")

    if current_url == "data:," or not current_url.startswith("http"):
        logger.info("Blank page detected. Navigating to login...")
        driver.get(LOGIN_URL)

    # If somehow still on blank page
    if driver.current_url == "data:,":
        logger.info("Page still blank after navigating. Reloading login...")
        driver.get(LOGIN_URL)

    return driver


def login_to_site():
    global driver

    try:
        driver = init_browser()

        if is_logged_in():
            logger.info("Already logged in, skipping login process")
            return True, "Already logged in."

        # THIS IS THE MISSING LINE - Navigate to login page!
        logger.info(f"Navigating to login page: {LOGIN_URL}")
        driver.get(LOGIN_URL)
        
        wait = WebDriverWait(driver, 10)

        # Looks for the username field
        logger.info("Looking for username field...")
        username_field = wait.until(
            EC.presence_of_element_located((By.ID, "MainContent_UserName"))
        )
        username_field.clear()
        username_field.send_keys(USERNAME)
        logger.info(f"Username entered: {USERNAME}")

        # Looks for the password field
        logger.info("Looking for password field...")
        password_field = wait.until(
            EC.presence_of_element_located((By.ID, "MainContent_Password"))
        )
        password_field.clear()
        password_field.send_keys(PASSWORD)
        logger.info("Password entered")

        # Looks and clicks on the login button for the next page
        logger.info("Looking for login button...")
        login_button = wait.until(
            EC.element_to_be_clickable((By.ID, "MainContent_LoginButton"))
        )
        login_button.click()
        logger.info("Login button clicked")
        
        time.sleep(5)

        # Wait for redirect to StockTaking page (next)
        logger.info("Waiting for redirect to StockTaking.aspx...")
        wait.until(EC.url_contains("StockTaking.aspx"))
        logger.info(f"Successfully logged in! Current URL: {driver.current_url}")

        return True, "Login successful."

    except Exception as e:
        error_msg = f"Login failed: {str(e)}"
        logger.error(error_msg)
        return False, error_msg


@app.route('/login', methods=['POST'])
def handle_login():
    logger.info("\n" + "="*50)
    logger.info("LOGIN REQUEST RECEIVED")
    logger.info("="*50)
    
    success, message = login_to_site()
    logger.info(f"Login result: Success={success}, Message={message}")
    
    return jsonify({"Success": success, "Message": message}), (200 if success else 500)



@app.route('/input_barcode', methods=['POST'])
def input_barcode():
    logger.info("\n" + "="*50)
    logger.info("BARCODE INPUT REQUEST RECEIVED")
    logger.info("="*50)

    try:
        data = request.get_json(force=True)
        barcode = data.get("barcode", "").strip()
        quantity = data.get("quantity")
        unit = data.get("unit")

        if not barcode:
            return jsonify({"Success": False, "Message": "Missing barcode"}), 400

        # NEW: Ensure the browser is ready (no success/message unpacking)
        driver = ensure_on_stocktaking_page()
        if driver is None:
            return jsonify({"Success": False, "Message": "Browser not ready"}), 500

        wait = WebDriverWait(driver, 10)

        # Barcode input
        code_box = wait.until(EC.presence_of_element_located((By.ID, "MainContent_txtNumberScan")))
        code_box.clear()
        code_box.send_keys(barcode)
        code_box.send_keys(Keys.ENTER)
        logger.info(f"Barcode '{barcode}' entered")

        # Quantity
        if quantity is not None:
            qty_box = wait.until(EC.presence_of_element_located((By.ID, "MainContent_txtQte")))
            qty_box.clear()
            qty_box.send_keys(str(quantity))
            logger.info(f"Quantity '{quantity}' entered")

        # Unit
        if unit:
            select_box = Select(wait.until(EC.presence_of_element_located((By.ID, "MainContent_cboUnite"))))
            select_box.select_by_visible_text(unit)
            logger.info(f"Unit '{unit}' selected")

        # Save button
        save_button = wait.until(EC.element_to_be_clickable((By.ID, "MainContent_btnAjouter")))
        save_button.click()
        logger.info("Save button clicked!")

        success_msg = f"Saved: {barcode}"
        if quantity:
            success_msg += f", Qty: {quantity}"
        if unit:
            success_msg += f" [{unit}]"

        return jsonify({"Success": True, "Message": success_msg}), 200

    except Exception as e:
        logger.error(f"Automation error: {e}", exc_info=True)
        return jsonify({"Success": False, "Message": f"Automation error: {str(e)}"}), 500


@app.route('/status', methods=['GET'])
def status():
    browser_active = driver is not None
    logger.info(f"Status check: Server running, Browser active: {browser_active}")
    logged_in = is_logged_in()
    logger.info(f"Status check: Server running, Browser active: {browser_active}, Logged in: {logged_in}")
    return jsonify({
        "Status": "running", 
        "BrowserActive": browser_active,
        "LoggedIn": logged_in
    }), 200


@app.route('/close', methods=['POST'])
def close_browser():
    global driver
    if driver:
        driver.quit()
        driver = None
        logger.info("Browser closed")
        return jsonify({"Message": "Browser closed"}), 200
    logger.info("No browser to close")
    return jsonify({"Message": "No browser to close"}), 200


if __name__ == "__main__":
    logger.info("="*50)
    logger.info("AUTOMATION SERVER STARTING")
    logger.info("="*50)
    logger.info(f"Server URL: http://192.168.50.225:5000")
    logger.info(f"Login URL: {LOGIN_URL}")
    logger.info(f"Username: {USERNAME}")
    logger.info("\nAvailable endpoints:")
    logger.info("  POST /login - Trigger login")
    logger.info("  POST /input_barcode - Send barcode data")
    logger.info("  GET  /status - Check server status")
    logger.info("  POST /close - Close browser")
    logger.info("="*50)
    
    # IMPORTANT: debug=False to prevent reloader from killing browser
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)