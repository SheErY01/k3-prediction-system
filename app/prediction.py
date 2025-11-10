import requests
from bs4 import BeautifulSoup
from datetime import datetime
import random
import os

BDG_URL = "https://pakgames.co/#/saasLottery/K3?gameCode=K3_1M&lottery=K3"

predictions_today = []
results_history = []
daily_stats = {'total': 0, 'correct': 0, 'wrong': 0, 'profit': 0}
MAX_DAILY_PREDICTIONS = 10
MAX_HISTORY_SIZE = 50

try:
    from app.k3_client import fetch_latest_draw
    USE_REAL_CLIENT = True
    print("✅ K3 Client loaded - will attempt real-time scraping")
except ImportError:
    USE_REAL_CLIENT = False
    print("⚠️ K3 Client not available - using mock data")

def scrape_results():
    """Scrape latest K3 results from pakgames.co.
    Uses Selenium-based client for real-time data when credentials are available.
    Falls back to mock data if scraping fails.
    """
    
    if USE_REAL_CLIENT and os.environ.get("PAKGAMES_USERNAME"):
        try:
            draw_data = fetch_latest_draw()
            if draw_data:
                if isinstance(draw_data.get('numbers'), list):
                    result_sum = draw_data.get('sum', 0)
                else:
                    result_sum = draw_data.get('sum', random.randint(3, 18))
                
                period = draw_data.get('period', f"2025110{len(results_history) + 1:04d}")
                
                result_data = {
                    'number': result_sum,
                    'period': period,
                    'time': draw_data.get('timestamp', datetime.now().isoformat()),
                    'raw_numbers': draw_data.get('numbers', [])
                }
                
                if len(results_history) == 0 or results_history[-1]['period'] != period:
                    results_history.append(result_data)
                    if len(results_history) > MAX_HISTORY_SIZE:
                        results_history.pop(0)
                    print(f"📥 Real K3 result: Period {period}, Sum {result_sum}, Numbers {draw_data.get('numbers', [])}")
                
                return result_data
        except Exception as e:
            print(f"⚠️ Real-time scraping error, falling back to mock: {e}")
    
    period = f"2025110{len(results_history) + 1:04d}"
    dice = [random.randint(1, 6), random.randint(1, 6), random.randint(1, 6)]
    number = sum(dice)
    result_data = {
        'number': number,
        'period': period,
        'time': datetime.now().isoformat(),
        'raw_numbers': dice
    }
    
    if len(results_history) == 0 or results_history[-1]['period'] != period:
        results_history.append(result_data)
        if len(results_history) > MAX_HISTORY_SIZE:
            results_history.pop(0)
        print(f"📥 Mock K3 result: Period {period}, Sum {number}, Dice {dice}")
    
    return result_data

def analyze_pattern(history):
    """Pattern analysis based on recent results history.
    Returns prediction number and confidence level.
    """
    if len(history) < 5:
        return None, 0

    last_results = [h['number'] for h in history[-10:]]
    
    if last_results[-5:].count(3) >= 2:
        return 18, 75
    elif last_results[-5:].count(18) >= 2:
        return 3, 80
    elif last_results[-3:].count(3) == 3:
        return 18, 85
    elif last_results[-3:].count(18) == 3:
        return 3, 90

    return None, 0
