import schedule
import time
import pyttsx3
import speech_recognition as sr
import re
from twilio.rest import Client  # Example SMS API (replace with desired API)

engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')

engine.setProperty('voice',voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

task_time=[]
task_description=[]
def get_user_input():
    
    while True:
        print("\nTime Schedule Manager")
        print("1. Add Task")
        print("2. Modify Task")
        print("3. Delete Task")
        print("4. Display task")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            description = input("Enter task description: ")
            scheduled_time = input("Enter scheduled time (HH:MM format): ")
            try:
                # Validate time format (replace XX with actual validation logic)
                # You can use regular expressions or time parsing libraries
                time_regex = r"^(?:[01]\d|2[0-3]):[0-5][0-9]$"  # Regular expression for HH:MM format
                if not re.match(time_regex, scheduled_time):
                    print("Invalid time format. Please use HH:MM.")
                    continue                

            except ValueError as e:
                print(e)
            task_time.append(scheduled_time)
            task_description.append(description)

        elif choice == '2':
            if not task_description:  # Check if any tasks exist
                print("No tasks found. Please add tasks first.")
                continue

            print("Tasks:")
            # Enumerate tasks for clear indexing (starts from 1)
            for index, (description, time) in enumerate(zip(task_description, task_time), start=1):
                print(f"{index}. {description} ({time})")
            modify_index = input("Enter the task number to modify (or 'q' to quit): ")
            if modify_index.lower() == 'q':
                continue
            try:
                modify_index = int(modify_index) - 1  # Convert to 0-based index
                if modify_index < 0 or modify_index >= len(task_description):
                    print("Invalid task number. Please try again.")
                    continue
                new_description = input("Enter new task description (or leave blank to keep existing): ")
                if new_description:
                    task_description[modify_index] = new_description

                new_time = input("Enter new scheduled time (HH:MM format, or leave blank to keep existing): ")

                if new_time:
                    # Validate new time if provided
                    if not re.match(time_regex, new_time):
                        print("Invalid new time format. Please use HH:MM (e.g., 09:30).")
                        continue
                task_time[modify_index] = new_time
                print("Task successfully modified.")

            except ValueError:
                print("Invalid input. Please enter a number or 'q' to quit.")


        elif choice == '3':
            if not task_description:
                print("No tasks found. Please add tasks first.")
                continue
            print("Tasks:")
            # Enumerate tasks for clear indexing (starts from 1)
            for index, (description, time) in enumerate(zip(task_description, task_time), start=1):
                print(f"{index}. {description} ({time})")

            delete_index = input("Enter the task number to delete (or 'q' to quit): ")
            if delete_index.lower() == 'q':
                continue
            try:
                delete_index = int(delete_index) - 1  # Convert to 0-based index
                if delete_index < 0 or delete_index >= len(task_description):
                    print("Invalid task number. Please try again.")
                    continue

                del task_description[delete_index]
                del task_time[delete_index]
                print("Task successfully deleted.")

            except ValueError:
                print("Invalid input. Please enter a number or 'q' to quit.")

        elif choice == '4':
             if not task_description:
                 print("No tasks found.")
             else:
                print("Tasks:")
                # Enumerate tasks for clear indexing (starts from 1)
                for index, (description, time) in enumerate(zip(task_description, task_time), start=1):
                    print(f"{index}. {description} ({time})")
           
        elif choice == '5':
            return
        else:
            print("Invalid choice. Please try again.")

def sentSms():
    for i in range(len(task_time)):
        account_sid = '************'
        auth_token = '*************'
        client = Client(account_sid, auth_token)
        
        message = client.messages.create(to='+91********',from_='+*************',body=f"Reminder: {task_description[i]} - Due at {task_time[i]}")
        speak("sir it's "+ task_time[i] + "hours......")
        speak( "reminder for " + task_description[i])


get_user_input()
sentSms()

