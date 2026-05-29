# backend/create_test_data.py
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Initialize the Firebase Admin SDK
# Make sure your service account JSON file is in the same directory
cred = credentials.Certificate("firebase-credentials.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# Data for the new user document
user_data = {
    "userId": "user_001",
    "email": "teen1@safeyouth.com",
    "nickname": "Alex",
    "ageRange": "16-18",
    "role": "teen",
    "isAnonymous": False,
    "createdAt": firestore.SERVER_TIMESTAMP # <-- This is the magic sentinel!
}

# Add the document to the 'users' collection
doc_ref = db.collection("users").add(user_data)

print(f"User document created successfully! Document ID: {doc_ref[1].id}")
print("The 'createdAt' field will be filled by the Firestore server.")