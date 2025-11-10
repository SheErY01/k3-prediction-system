# K3 Prediction System

## Overview
This is a K3 lottery prediction system that combines web scraping, pattern analysis, and automated email notifications. The system runs continuously, analyzing patterns and sending predictions when confidence thresholds are met.

## Architecture
- **Language**: Python 3.11
- **Framework**: Flask (web server)
- **Port**: 5000 (Flask web interface)
- **Background Tasks**: Schedule library for periodic tasks

## Core Components
1. **Flask App** (`app/flask_app.py`) - Web server with health check endpoint
2. **Prediction Engine** (`app/prediction.py`) - Scrapes K3 results and analyzes patterns
3. **Email Service** (`app/email_service.py`) - Sends Gmail notifications for predictions and summaries
4. **Scheduler** (`app/scheduler.py`) - Runs periodic tasks:
   - Every 1 minute: Make predictions
   - Every 1 minute: Verify previous predictions
   - Daily at 22:00: Send daily summary email

## Environment Variables Required
The following environment variables need to be set for email functionality:
- `GMAIL_USER` - Gmail address for sending emails
- `GMAIL_APP_PASSWORD` - Gmail app password (not regular password)
- `RECIPIENT_EMAIL` - Email address to receive alerts (defaults to GMAIL_USER)
- `PORT` - Optional, defaults to 5000

## Recent Changes (Nov 5, 2025)
- Initial import from GitHub
- Installed Python 3.11 and all dependencies (Flask, requests, beautifulsoup4, schedule)
- Created .gitignore for Python project
- Configured workflow for Flask web server on port 5000
- **Updated scraping URL** from bdgwinvip9.com to https://www.paklotto.asia/#/
- **Created real-time web dashboard** with beautiful purple gradient UI
- **Removed email service dependency** - all alerts now shown on web interface
- **Fixed prediction logic** - system now maintains results history and generates predictions correctly
- Added API endpoints for real-time data access (/api/predictions, /api/stats)
- Implemented mock data generation for testing when actual scraping fails
- Added auto-refresh functionality (updates every 5 seconds)
- Configured deployment for VM target (continuous operation)

## How It Works
1. **Scraper** fetches lottery results every minute (currently using mock data for testing)
2. **Results history** is maintained (up to 50 recent results)
3. **Pattern analyzer** examines the last 5-10 results to identify patterns
4. **Predictions** are generated when confidence >= 70%
5. **Web dashboard** displays predictions in real-time with stats and visualization
6. **Verification** happens automatically when new results match prediction periods

## Important Notes
- Email functionality has been removed - all data displayed on web interface
- Web scraping currently uses mock/demo data for testing (selectors need updating for real site)
- Prediction algorithm is pattern-based (analyzes frequency of numbers 3 and 18)
- Maximum 10 predictions per day (configurable via MAX_DAILY_PREDICTIONS)
- System runs continuously and updates dashboard every 5 seconds
