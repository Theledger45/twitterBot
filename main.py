import tweepy          # Import the Tweepy library for interacting with the Twitter API
import requests        # Import requests to handle HTTP requests
import os              # Import os to interact with the operating system (e.g., environment variables)
import pytz            # Import pytz for timezone calculations
import threading       # Import threading for running tasks in separate threads
import schedule        # Import schedule for scheduling tasks at specific times
from timezonefinder import TimezoneFinder  # Import TimezoneFinder to find time zones based on latitude and longitude
from datetime import datetime, timedelta   # Import datetime for handling dates and times
from dotenv import load_dotenv             # Import load_dotenv to load environment variables from a .env file
import tkinter as tk                       # Import tkinter for GUI elements
from tkinter import messagebox, filedialog, scrolledtext  # Import specific tkinter modules
from tkinter import ttk                    # Import ttk for themed tkinter widgets
from tkcalendar import DateEntry           # Import DateEntry for date selection widget
from PIL import Image, ImageTk             # Import PIL for image handling in the GUI

# Load environment variables from a .env file (e.g., Twitter API keys)
load_dotenv()

# Twitter API credentials retrieved from environment variables
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

# Authenticate with the Twitter API using OAuth 1.0a
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)  # Create an API object to interact with Twitter

# Create the main application window
root = tk.Tk()
root.title("Twitter Scheduler")          # Set the window title
root.geometry("450x750")                 # Set the window size
root.configure(bg="white")               # Set background color to white

# Variable to hold the path of the selected image for media attachments
selected_image_path = tk.StringVar()

def tweet_message_v2(message):
    """
    Function to send a tweet with or without media attachment.
    """
    media_path = selected_image_path.get()  # Get the selected image path
    if media_path:
        # If media is selected, tweet with media
        tweet = api.update_status_with_media(filename=media_path, status=message)
    else:
        # If no media, tweet only the message
        tweet = api.update_status(status=message)
    tweet_id = tweet.id  # Get the tweet ID
    # Show a message box confirming the tweet was sent
    messagebox.showinfo("Tweet Sent", f"Tweet posted successfully! Tweet ID: {tweet_id}")

def get_timezone_from_zip(zip_code):
    """
    Function to retrieve timezone information based on a US zip code.
    """
    try:
        # Send a request to the Zippopotam.us API with the provided zip code
        response = requests.get(f"http://api.zippopotam.us/us/{zip_code}")
        response.raise_for_status()  # Raise an error if the request was unsuccessful
        data = response.json()       # Parse the JSON data

        # Extract latitude and longitude from the API response
        latitude = float(data['places'][0]['latitude'])
        longitude = float(data['places'][0]['longitude'])

        # Use TimezoneFinder to find the timezone based on latitude and longitude
        tf = TimezoneFinder()
        timezone = tf.timezone_at(lat=latitude, lng=longitude)
        
        if timezone:
            timezone_var.set(timezone)  # Update the timezone dropdown with the found timezone
        else:
            # If timezone is not found, display an error message
            messagebox.showerror("Error", "Timezone not found for this location.")
    except requests.exceptions.RequestException:
        # Handle exceptions (e.g., invalid zip code or network issues)
        messagebox.showerror("Error", "Invalid Zip Code or API error. Please try again.")

def run_at_datetime(target_datetime, message, interval_type=None):
    """
    Function to schedule the tweet at the specified date and time, with optional recurrence.
    """
    def job():
        tweet_message_v2(message)  # Function to execute when the scheduled time arrives

    now = datetime.now(target_datetime.tzinfo)  # Current time in the target timezone
    time_remaining = (target_datetime - now).total_seconds()  # Calculate time until the scheduled time
    
    if interval_type == "Every day":
        schedule.every().day.at(target_datetime.strftime("%H:%M")).do(job)
        messagebox.showinfo("Scheduled", "Recurring tweet scheduled for every day.")
    elif interval_type == "Every week":
        schedule.every().week.at(target_datetime.strftime("%H:%M")).do(job)
        messagebox.showinfo("Scheduled", "Recurring tweet scheduled for every week.")
    elif interval_type == "Every month":
        schedule.every(4).weeks.at(target_datetime.strftime("%H:%M")).do(job)
        messagebox.showinfo("Scheduled", "Recurring tweet scheduled for every month.")
    elif interval_type == "Every minute":
        schedule.every(1).minute.do(job)
        messagebox.showinfo("Scheduled", "Recurring tweet scheduled for every minute.")
    elif interval_type == "Every hour":
        schedule.every(1).hour.do(job)
        messagebox.showinfo("Scheduled", "Recurring tweet scheduled for every hour.")
    else:
        # If no recurrence, schedule the tweet to run after the time remaining
        threading.Timer(time_remaining, job).start()
        messagebox.showinfo("Scheduled", f"Tweet scheduled for {target_datetime.strftime('%Y-%m-%d %I:%M %p %Z')}.")

def start_scheduling():
    """
    Function to initiate the scheduling process based on user input from the GUI.
    """
    selected_date = date_entry.get_date()       # Get the selected date from the DateEntry widget
    selected_time = time_entry.get()            # Get the entered time from the time Entry widget
    selected_timezone = timezone_var.get()      # Get the selected timezone
    message = message_entry.get("1.0", "end-1c")  # Get the message text from the scrolled text widget
    am_pm = am_pm_var.get()                     # Get AM/PM selection
    interval_type = interval_type_var.get()     # Get the interval type for recurrence

    # Parse the hour and minute from the entered time
    hour, minute = map(int, selected_time.split(":"))
    # Adjust hour based on AM/PM selection
    if am_pm == "PM" and hour != 12:
        hour += 12
    elif am_pm == "AM" and hour == 12:
        hour = 0

    # Create a datetime object with the selected date and time
    target_datetime = datetime(selected_date.year, selected_date.month, selected_date.day, hour, minute)
    target_timezone = pytz.timezone(selected_timezone)        # Get the pytz timezone object
    target_datetime = target_timezone.localize(target_datetime)  # Localize the datetime object to the selected timezone

    # Call the function to schedule the tweet
    run_at_datetime(target_datetime, message, interval_type)

def select_image():
    """
    Function to open a file dialog for selecting an image and display a preview in the GUI.
    """
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")])
    if file_path:
        img = Image.open(file_path)                 # Open the selected image
        img.thumbnail((100, 100))                   # Resize the image to fit in the GUI
        img = ImageTk.PhotoImage(img)               # Convert the image to a format usable by Tkinter
        image_label.config(image=img)               # Update the image label with the new image
        image_label.image = img                     # Keep a reference to avoid garbage collection
        selected_image_path.set(file_path)          # Store the image path for later use

# GUI Elements

# Title label at the top of the window
title_label = tk.Label(
    root,
    text="Twitter Scheduler",
    font=("Arial", 20, "bold"),
    fg="#1DA1F2",
    bg="white"
)
title_label.pack(pady=20)

# Label and entry for the zip code
zip_label = tk.Label(
    root,
    text="Enter Zip Code (optional):",
    font=("Arial", 12),
    fg="black",
    bg="white"
)
zip_label.pack(pady=5)
zip_entry = tk.Entry(
    root,
    font=("Arial", 12),
    bg="#E8F5FD",
    fg="black"
)
zip_entry.pack()

# Button to fetch the timezone based on the entered zip code
zip_button = tk.Button(
    root,
    text="Get Timezone from Zip",
    font=("Arial", 12),
    bg="#1DA1F2",
    fg="white",
    command=lambda: get_timezone_from_zip(zip_entry.get())
)
zip_button.pack(pady=5)

# Label and date picker for selecting the date
date_label = tk.Label(
    root,
    text="Select Date:",
    font=("Arial", 12),
    fg="black",
    bg="white"
)
date_label.pack(pady=5)
date_entry = DateEntry(
    root,
    width=12,
    background='darkblue',
    foreground='white',
    borderwidth=2,
    mindate=datetime.now()  # Set the minimum date to today
)
date_entry.pack()

# Label and time entry for entering the time
time_label = tk.Label(
    root,
    text="Enter Time:",
    font=("Arial", 12),
    fg="black",
    bg="white"
)
time_label.pack(pady=5)
time_frame = tk.Frame(root, bg="white")
time_frame.pack()
time_entry = tk.Entry(
    time_frame,
    font=("Arial", 12),
    width=5,
    bg="#E8F5FD",
    fg="black"
)
time_entry.insert(0, "12:00")  # Default time
time_entry.pack(side="left")

# Dropdown for selecting AM or PM
am_pm_var = tk.StringVar(value="AM")
am_pm_dropdown = ttk.Combobox(
    time_frame,
    textvariable=am_pm_var,
    values=["AM", "PM"],
    state="readonly",
    width=5
)
am_pm_dropdown.pack(side="left", padx=5)

# Label and dropdown for selecting the timezone
timezone_label = tk.Label(
    root,
    text="Select Time Zone:",
    font=("Arial", 12),
    fg="black",
    bg="white"
)
timezone_label.pack(pady=5)
timezone_var = tk.StringVar()
timezone_dropdown = ttk.Combobox(
    root,
    textvariable=timezone_var,
    values=pytz.all_timezones,
    state="readonly",
    width=30
)
timezone_dropdown.set("UTC")  # Default timezone
timezone_dropdown.pack()

# Label and dropdown for selecting the interval type (e.g., one-time, daily)
interval_type_label = tk.Label(
    root,
    text="Select Interval Type:",
    font=("Arial", 12),
    fg="black",
    bg="white"
)
interval_type_label.pack(pady=5)
interval_type_var = tk.StringVar(value="One-time")
interval_type_dropdown = ttk.Combobox(
    root,
    textvariable=interval_type_var,
    values=["One-time", "Every day", "Every week", "Every month", "Every minute", "Every hour"],
    state="readonly",
    width=15
)
interval_type_dropdown.pack()

# Label and text area for entering the tweet message
message_label = tk.Label(
    root,
    text="Enter your message:",
    font=("Arial", 12),
    fg="black",
    bg="white"
)
message_label.pack(pady=5)
message_entry = scrolledtext.ScrolledText(
    root,
    font=("Arial", 12),
    height=4,
    width=30,
    bg="#E8F5FD",
    fg="black",
    insertbackground="black"  # Cursor color
)
message_entry.pack()

# Button to select an image for the tweet
image_button = tk.Button(
    root,
    text="Select Image",
    font=("Arial", 12),
    command=select_image,
    bg="#1DA1F2",
    fg="white"
)
image_button.pack(pady=5)

# Label to display the selected image preview
image_label = tk.Label(root, bg="white")
image_label.pack()

# Button to schedule the tweet based on the entered information
schedule_button = tk.Button(
    root,
    text="Schedule Tweet",
    font=("Arial", 14),
    bg="#1DA1F2",
    fg="white",
    command=start_scheduling
)
schedule_button.pack(pady=20)

# Start the main event loop to run the application
root.mainloop()
