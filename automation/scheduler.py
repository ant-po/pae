import schedule
import subprocess
import time

def job():
    print("Running daily strategy...")
    subprocess.call(["python", "main.py"])
    subprocess.call(["python", "backtester.py"])

schedule.every().day.at("06:00").do(job)
schedule.every().day.at("18:00").do(job)

if __name__ == "__main__":
    print("Scheduler started. Waiting for next run...")
    while True:
        schedule.run_pending()
        time.sleep(60)