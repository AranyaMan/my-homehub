#!/usr/bin/env python3
"""
Background scheduler for push notifications.
Run this as a separate process or integrate with your process manager (systemd, supervisor, etc.)
"""
import os
import sys
import time
import signal
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app import create_app
from app.blueprints.chores import send_chore_notifications


def run_notification_job():
    """Wrapper to run notification job with app context."""
    app = create_app()
    with app.app_context():
        try:
            result = send_chore_notifications()
            print(f"[{datetime.now()}] Push notifications: sent={result.get('sent', 0)}, errors={len(result.get('errors', []))}")
            if result.get('errors'):
                for err in result['errors']:
                    print(f"  ERROR: {err}")
        except Exception as e:
            print(f"[{datetime.now()}] Push notification job failed: {e}")


def main():
    print("Starting HomeHub Push Notification Scheduler...")
    print(f"Time: {datetime.now()}")
    
    # Create scheduler
    scheduler = BackgroundScheduler(timezone='UTC')
    
    # Run every hour at minute 0 (adjust as needed)
    # For testing, you might want every 5 minutes: CronTrigger(minute='*/5')
    scheduler.add_job(
        run_notification_job,
        CronTrigger(minute=0),  # Run at minute 0 of every hour
        id='chore_push_notifications',
        name='Chore Due Push Notifications',
        replace_existing=True
    )
    
    # Also run once at startup for testing
    scheduler.add_job(
        run_notification_job,
        'date',
        run_date=datetime.now(),
        id='startup_notification_check'
    )
    
    scheduler.start()
    print("Scheduler started. Press Ctrl+C to stop.")
    print("Jobs:")
    for job in scheduler.get_jobs():
        print(f"  - {job.name}: {job.trigger}")
    
    # Handle graceful shutdown
    def shutdown(signum, frame):
        print("\nShutting down scheduler...")
        scheduler.shutdown()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)
    
    # Keep running
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        shutdown(None, None)


if __name__ == '__main__':
    main()