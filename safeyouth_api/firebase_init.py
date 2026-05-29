# backend/safeyouth_api/firebase_init.py

import firebase_admin
from firebase_admin import credentials, firestore, auth, messaging
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Firebase
cred = credentials.Certificate('firebase-credentials.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'safeyouth-ai.firebasestorage.app'
})

# Get Firestore client
db = firestore.client()

# Get Auth client
firebase_auth = auth

# Get Messaging client
fcm = messaging

def verify_firebase_token(token):
    """Verify Firebase ID token"""
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        return None

def send_push_notification(user_id, title, body, data=None):
    """Send push notification to user"""
    try:
        # Get user's FCM token from Firestore
        user_ref = db.collection('users').document(user_id)
        user = user_ref.get()
        
        if user.exists and 'fcm_token' in user.to_dict():
            token = user.to_dict()['fcm_token']
            
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body,
                ),
                data=data or {},
                token=token,
            )
            
            response = messaging.send(message)
            return response
    except Exception as e:
        print(f"Error sending notification: {e}")
        return None