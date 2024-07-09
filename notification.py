import firebase_admin
from firebase_admin import credentials, messaging
import time
from datetime import datetime, timedelta
import pytz
from google.cloud import firestore

# Initialize the Firebase Admin SDK
cred = credentials.Certificate("mini-project-6a07a-firebase-adminsdk-k0g95-aa209caeee.json")
firebase_admin.initialize_app(cred)

def send_fcm_notification(device_token, title, body, data=None):
    # Create the notification message
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=device_token,
        data=data if data else {}
    )

    # Send the notification
    response = messaging.send(message)
    print('Successfully sent message:', response)



def initialize_firestore():
    # Replace 'path/to/serviceAccountKey.json' with the path to your service account key JSON file
    firestore_client = firestore.Client.from_service_account_json('mini-project-6a07a-firebase-adminsdk-k0g95-aa209caeee.json')
    return firestore_client

# Get current Indian time
def get_indian_time():
    india_tz = pytz.timezone('Asia/Kolkata')
    return datetime.now(india_tz)

# Fetch data from Firestore
def fetch_data(firestore_client):
    current_time = get_indian_time()
    start_time = current_time - timedelta(seconds=30)
    
    # Convert to Firestore timestamp format
    start_time = start_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    end_time = current_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    
    # Replace 'your_collection_name' and 'date_time_field' with your actual collection name and field name
    collection_ref = firestore_client.collection('notifications')
    query = collection_ref.where('datetime', '>=', start_time).where('datetime', '<=', end_time)
    print(end_time)
    print(start_time)
    docs = query.stream()
    print(docs)
    for doc in docs:
       data = doc.to_dict()
       send_fcm_notification(data["device_id"],data["title"],data["body"])

# Function to call fetch_data every 2 minutes
def call_every_two_minutes( firestore_client):
    try:
        while True:
            fetch_data(firestore_client)
            time.sleep(30)  # Sleep for 120 seconds (2 minutes)
    except KeyboardInterrupt:
        print("Script interrupted by user. Exiting gracefully...")

# Example usage
if __name__ == "__main__":
    firestore_client = initialize_firestore()
    call_every_two_minutes( firestore_client)



