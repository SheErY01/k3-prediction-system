import schedule
import time
from datetime import datetime
from app.prediction import scrape_results, analyze_pattern, predictions_today, daily_stats, MAX_DAILY_PREDICTIONS, results_history

def make_prediction():
    if daily_stats['total'] >= MAX_DAILY_PREDICTIONS:
        return

    data = scrape_results()
    if not data:
        return

    prediction, confidence = analyze_pattern(results_history)
    if prediction and confidence >= 70:
        for pred in predictions_today:
            if pred.get('period') == data['period'] and not pred.get('verified'):
                return
        
        print(f"🎯 Prediction Alert - Number: {prediction}, Period: {data['period']}, Time: {datetime.now().strftime('%I:%M %p')}, Confidence: {confidence}%")
        predictions_today.append({
            'number': prediction,
            'period': data['period'],
            'time': datetime.now().isoformat(),
            'confidence': confidence,
            'verified': False
        })
        daily_stats['total'] += 1

def verify_predictions():
    data = scrape_results()
    if not data:
        return

    for pred in predictions_today:
        if not pred.get('verified') and pred['period'] == data['period']:
            correct = pred['number'] == data['number']
            pred['verified'] = True
            pred['correct'] = correct

            if correct:
                daily_stats['correct'] += 1
                daily_stats['profit'] += 60
            else:
                daily_stats['wrong'] += 1
                daily_stats['profit'] -= 60

def reset_daily_summary():
    if daily_stats['total'] > 0:
        accuracy = (daily_stats['correct'] / daily_stats['total']) * 100
        summary = (
            f"📊 Daily Summary - {datetime.now().date()}\n"
            f"Total: {daily_stats['total']}\n"
            f"✅ Correct: {daily_stats['correct']}\n"
            f"❌ Wrong: {daily_stats['wrong']}\n"
            f"🎯 Accuracy: {accuracy:.2f}%\n"
            f"💰 Profit: ₹{daily_stats['profit']}"
        )
    else:
        summary = "No predictions made today. System was monitoring."

    print(summary)
    predictions_today.clear()
    daily_stats.update({'total': 0, 'correct': 0, 'wrong': 0, 'profit': 0})

def start_scheduler():
    schedule.every(1).minutes.do(make_prediction)
    schedule.every(1).minutes.do(verify_predictions)
    schedule.every().day.at("22:00").do(reset_daily_summary)

    print("✅ Scheduler started - Monitoring for predictions every minute")
    while True:
        schedule.run_pending()
        time.sleep(1)
