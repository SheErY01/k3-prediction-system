import requests
from bs4 import BeautifulSoup
from datetime import datetime

BDG_URL = "https://pakgames.co/#/saasLottery/K3?gameCode=K3_1M&lottery=K3"

predictions_today = []
results_history = []
daily_stats = {'total': 0, 'correct': 0, 'wrong': 0, 'profit': 0}
MAX_DAILY_PREDICTIONS = 10
MAX_HISTORY_SIZE = 50

def scrape_results():
    """Scrape latest K3 results from BDG site.
    NOTE: Update CSS selectors based on the real site structure.
    For now, returns mock data for testing/fallback purposes.
    """
    import random
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(BDG_URL, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # PLACEHOLDERS - replace with actual selectors after inspecting site
        result_el = soup.select_one('.result-class')
        period_el = soup.select_one('.period-class')

        if result_el and period_el:
            result = int(result_el.text.strip())
            period = period_el.text.strip()
            result_data = {'number': result, 'period': period, 'time': datetime.now().isoformat()}
            
            if len(results_history) == 0 or results_history[-1]['period'] != period:
                results_history.append(result_data)
                if len(results_history) > MAX_HISTORY_SIZE:
                    results_history.pop(0)
                print(f"📥 New result from site: Period {period}, Number {result}")
            
            return result_data

    except Exception as e:
        print(f"⚠️ Scraping error (using mock data): {e}")
    
    period = f"2025110{len(results_history) + 1:04d}"
    number = random.choice([3, 18, 5, 7, 12, 15, 20])
    result_data = {'number': number, 'period': period, 'time': datetime.now().isoformat()}
    
    if len(results_history) == 0 or results_history[-1]['period'] != period:
        results_history.append(result_data)
        if len(results_history) > MAX_HISTORY_SIZE:
            results_history.pop(0)
        print(f"📥 New mock result: Period {period}, Number {number}")
    
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
