import time
import winsound
import datetime

def play_alert():
    # Play a beep sound at 1000Hz for 1 second
    frequency = 1000  # Hz
    duration = 1000   # milliseconds
    winsound.Beep(frequency, duration)

def timer(minutes=10):
    interval = minutes * 60  # Convert minutes to seconds
    
    print(f"Timer started for {minutes} minutes intervals")
    
    while True:
        # Sleep for the specified interval
        time.sleep(interval)
        
        # Get current time
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        
        # Play sound and show notification
        play_alert()
        print(f"Time's up! [{current_time}]")

if __name__ == "__main__":
    try:
        timer(10)  # Start timer with 10 minutes interval
    except KeyboardInterrupt:
        print("\nTimer stopped by user")