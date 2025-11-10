import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from datetime import datetime
import os
import json
import time

try:
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.core.os_manager import ChromeType
    WEBDRIVER_MANAGER_AVAILABLE = True
except ImportError:
    WEBDRIVER_MANAGER_AVAILABLE = False

K3_URL = "https://pakgames.co/#/saasLottery/K3?gameCode=K3_1M&lottery=K3"

class K3Client:
    def __init__(self):
        self.driver = None
        self.username = os.environ.get("PAKGAMES_USERNAME", "")
        self.password = os.environ.get("PAKGAMES_PASSWORD", "")
        
    def setup_driver(self):
        if self.driver:
            return
            
        chrome_options = Options()
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-setuid-sandbox')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--allow-running-insecure-content')
        chrome_options.add_argument('--disable-features=IsolateOrigins,site-per-process')
        chrome_options.add_argument('--remote-debugging-port=9222')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        chrome_options.page_load_strategy = 'eager'
        
        chromium_path = '/nix/store/qa9cnw4v5xkxyip6mb9kxqfq1z4x2dx1-chromium-138.0.7204.100/bin/chromium'
        if os.path.exists(chromium_path):
            chrome_options.binary_location = chromium_path
        
        try:
            if WEBDRIVER_MANAGER_AVAILABLE:
                print("🔧 Using webdriver-manager to install chromedriver...")
                service = Service(
                    ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
                )
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                print("✅ Selenium WebDriver initialized with webdriver-manager")
            else:
                service = Service()
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                print("✅ Selenium WebDriver initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize WebDriver: {e}")
            print(f"   Falling back to mock data for lottery results")
            self.driver = None
    
    def login(self):
        if not self.driver or not self.username or not self.password:
            return False
            
        try:
            self.driver.get("https://pakgames.co/#/login")
            time.sleep(2)
            
            phone_input = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder*='Phone']")
            phone_input.send_keys(self.username)
            
            password_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            password_input.send_keys(self.password)
            
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            
            time.sleep(3)
            print("✅ Login successful")
            return True
            
        except Exception as e:
            print(f"❌ Login failed: {e}")
            return False
    
    def fetch_latest_draw(self):
        if not self.driver:
            self.setup_driver()
            
        if not self.driver:
            return None
            
        try:
            if self.username and self.password:
                self.login()
            
            self.driver.get(K3_URL)
            time.sleep(3)
            
            wait = WebDriverWait(self.driver, 10)
            
            period_element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[class*='period'], [class*='issue'], [class*='draw']"))
            )
            period = period_element.text.strip()
            
            result_elements = self.driver.find_elements(By.CSS_SELECTOR, "[class*='result'] [class*='number'], [class*='dice']")
            
            if result_elements:
                numbers = [elem.text.strip() for elem in result_elements[:3]]
                result_sum = sum([int(n) for n in numbers if n.isdigit()])
                
                draw_data = {
                    'period': period,
                    'numbers': numbers,
                    'sum': result_sum,
                    'timestamp': datetime.now().isoformat()
                }
                
                print(f"✅ Fetched real draw: Period {period}, Numbers {numbers}, Sum {result_sum}")
                return draw_data
            
        except Exception as e:
            print(f"⚠️ Selenium scraping error: {e}")
            
        return None
    
    def get_performance_logs(self):
        if not self.driver:
            return []
        
        try:
            logs = self.driver.execute_script(
                "var performance = window.performance || {}; "
                "var network = performance.getEntries() || []; "
                "return network;"
            )
            return logs
        except:
            return []
    
    def extract_api_endpoint(self):
        if not self.driver:
            self.setup_driver()
            
        if not self.driver:
            return None
            
        try:
            self.driver.get(K3_URL)
            time.sleep(5)
            
            logs = self.driver.get_log('performance')
            
            for log in logs:
                message = json.loads(log['message'])
                method = message.get('message', {}).get('method', '')
                
                if 'Network.response' in method:
                    params = message.get('message', {}).get('params', {})
                    response_url = params.get('response', {}).get('url', '')
                    
                    if 'k3' in response_url.lower() or 'lottery' in response_url.lower() or 'result' in response_url.lower():
                        print(f"🔍 Found API endpoint: {response_url}")
                        return response_url
            
        except Exception as e:
            print(f"⚠️ API extraction error: {e}")
        
        return None
    
    def cleanup(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

k3_client = K3Client()

def fetch_latest_draw():
    return k3_client.fetch_latest_draw()

def cleanup_client():
    k3_client.cleanup()
