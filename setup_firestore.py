# backend/setup_firestore.py

import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta
import random

# Initialize Firebase
cred = credentials.Certificate('firebase-credentials.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def create_users_collection():
    """Create users collection with sample data"""
    users = [
        {
            "userId": "user_001",
            "email": "teen1@safeyouth.com",
            "nickname": "Alex",
            "ageRange": "16-18",
            "role": "teen",
            "location": {
                "region": "Bono",
                "town": "Jenjemireja",
                "coordinates": {"lat": 7.9465, "lng": -2.3456}
            },
            "createdAt": firestore.SERVER_TIMESTAMP,
            "isAnonymous": False
        },
        {
            "userId": "user_002",
            "email": "teen2@safeyouth.com",
            "nickname": "Maya",
            "ageRange": "13-15",
            "role": "teen",
            "location": {
                "region": "Bono",
                "town": "Sunyani",
                "coordinates": {"lat": 7.3369, "lng": -2.3308}
            },
            "createdAt": firestore.SERVER_TIMESTAMP,
            "isAnonymous": False
        },
        {
            "userId": "user_003",
            "email": "counselor@safeyouth.com",
            "nickname": "Counselor Jane",
            "ageRange": "25+",
            "role": "counselor",
            "location": {
                "region": "Bono",
                "town": "Techiman",
                "coordinates": {"lat": 7.5898, "lng": -1.9349}
            },
            "createdAt": firestore.SERVER_TIMESTAMP,
            "isAnonymous": False
        }
    ]
    
    for user in users:
        db.collection('users').add(user)
        print(f"Added user: {user['nickname']}")

def create_mood_logs():
    """Create sample mood logs"""
    moods = [
        {"moodScore": 5, "moodLabel": "happy", "note": "Had a great day!"},
        {"moodScore": 2, "moodLabel": "sad", "note": "Feeling lonely"},
        {"moodScore": 3, "moodLabel": "anxious", "note": "Worried about exams"},
        {"moodScore": 4, "moodLabel": "calm", "note": "Meditation helped"},
        {"moodScore": 1, "moodLabel": "angry", "note": "Felt pressured by friends"}
    ]
    
    for i, mood in enumerate(moods):
        mood_log = {
            "userId": "user_001",
            "moodScore": mood["moodScore"],
            "moodLabel": mood["moodLabel"],
            "note": mood["note"],
            "triggers": random.choice([["peer_pressure"], ["school"], ["family"], ["drugs"]]),
            "date": datetime.now() - timedelta(days=i)
        }
        db.collection('mood_logs').add(mood_log)
        print(f"Added mood log: {mood['moodLabel']}")

def create_opportunities():
    """Create sample opportunities for youth"""
    opportunities = [
        {
            "title": "Digital Skills Training Program",
            "category": "training",
            "description": "Free 3-month coding bootcamp for youth in Bono Region",
            "deadline": datetime(2025, 1, 31, 23, 59, 59),
            "link": "https://example.com/digital-skills",
            "location": "Online + In-person at Sunyani",
            "stipend": "Monthly allowance of GHS 500",
            "requirements": ["Age 15-25", "Basic English literacy", "Commitment to 3 months"],
            "isActive": True
        },
        {
            "title": "Scholarship for Girls in STEM",
            "category": "scholarship",
            "description": "Full scholarship for female students pursuing STEM education",
            "deadline": datetime(2025, 2, 15, 23, 59, 59),
            "link": "https://example.com/stem-scholarship",
            "location": "Nationwide",
            "stipend": "Full tuition + GHS 1000 stipend",
            "requirements": ["Female", "Age 13-19", "Good academic record"],
            "isActive": True
        },
        {
            "title": "Youth Entrepreneurship Grant",
            "category": "job",
            "description": "Startup grant for young entrepreneurs with business ideas",
            "deadline": datetime(2025, 3, 1, 23, 59, 59),
            "link": "https://example.com/entrepreneurship",
            "location": "Bono Region",
            "stipend": "Seed funding up to GHS 5000",
            "requirements": ["Business plan required", "Age 16-25"],
            "isActive": True
        }
    ]
    
    for opp in opportunities:
        db.collection('opportunities').add(opp)
        print(f"Added opportunity: {opp['title']}")

def create_learning_modules():
    """Create educational content modules"""
    modules = [
        {
            "title": "How to Say No to Peer Pressure",
            "category": "life_skills",
            "content": {
                "videoUrl": "https://example.com/videos/peer-pressure",
                "text": "Learn effective strategies to resist peer pressure...",
                "quiz": [
                    {"question": "What's the best way to say no?", "options": ["A", "B", "C"], "answer": "A"}
                ],
                "resources": ["Helpline: 112", "Local support groups"]
            },
            "duration": 15,
            "isOfflineAvailable": True,
            "points": 100
        },
        {
            "title": "Understanding Drug Effects: Tramadol & Weed",
            "category": "drug_awareness",
            "content": {
                "videoUrl": "https://example.com/videos/drug-awareness",
                "text": "Learn about the real effects of drugs on your body and mind...",
                "quiz": [],
                "resources": ["NACOP Helpline: 0800-111-222"]
            },
            "duration": 20,
            "isOfflineAvailable": True,
            "points": 150
        },
        {
            "title": "Mental Health and Self-Care",
            "category": "mental_health",
            "content": {
                "videoUrl": "https://example.com/videos/mental-health",
                "text": "Tips for maintaining good mental health...",
                "quiz": [],
                "resources": ["Mental Health Helpline: 193"]
            },
            "duration": 12,
            "isOfflineAvailable": True,
            "points": 120
        },
        {
            "title": "Start a Small Business",
            "category": "career",
            "content": {
                "videoUrl": "https://example.com/videos/business",
                "text": "Step-by-step guide to starting your own business...",
                "quiz": [],
                "resources": ["Youth Enterprise Support"]
            },
            "duration": 25,
            "isOfflineAvailable": True,
            "points": 200
        }
    ]
    
    for module in modules:
        db.collection('learning_modules').add(module)
        print(f"Added module: {module['title']}")

def create_drug_hotspots():
    """Create sample drug activity hotspots"""
    hotspots = [
        {
            "location": {
                "region": "Bono",
                "town": "Jenjemireja",
                "coordinates": {"lat": 7.9465, "lng": -2.3456}
            },
            "reports": 12,
            "riskLevel": "high",
            "lastReported": datetime.now()
        },
        {
            "location": {
                "region": "Bono",
                "town": "Sunyani",
                "coordinates": {"lat": 7.3369, "lng": -2.3308}
            },
            "reports": 5,
            "riskLevel": "medium",
            "lastReported": datetime.now() - timedelta(days=2)
        },
        {
            "location": {
                "region": "Bono",
                "town": "Techiman",
                "coordinates": {"lat": 7.5898, "lng": -1.9349}
            },
            "reports": 3,
            "riskLevel": "low",
            "lastReported": datetime.now() - timedelta(days=5)
        }
    ]
    
    for hotspot in hotspots:
        db.collection('drug_hotspots').add(hotspot)
        print(f"Added hotspot: {hotspot['location']['town']}")

def setup_security_rules():
    """Create Firestore security rules (via Python)"""
    # Note: Security rules must be set in Firebase Console
    print("""
    ⚠️ IMPORTANT: Set up security rules in Firebase Console:
    
    1. Go to Firestore Database → Rules
    2. Add the following rules:
    
    rules_version = '2';
    service cloud.firestore {
      match /databases/{database}/documents {
        // Users can read/write their own data
        match /users/{userId} {
          allow read, write: if request.auth != null && request.auth.uid == userId;
        }
        
        // Anyone can read opportunities and learning modules
        match /opportunities/{document} {
          allow read: if true;
          allow write: if request.auth != null && request.auth.token.role == 'admin';
        }
        
        match /learning_modules/{document} {
          allow read: if true;
          allow write: if request.auth != null && request.auth.token.role == 'admin';
        }
        
        // Help requests - teens can create, counselors can view assigned
        match /help_requests/{requestId} {
          allow create: if request.auth != null;
          allow read: if request.auth != null && 
            (request.auth.uid == resource.data.userId || 
             request.auth.token.role == 'counselor' ||
             request.auth.token.role == 'admin');
        }
        
        // Mood logs - private to user
        match /mood_logs/{logId} {
          allow read, write: if request.auth != null && request.auth.uid == resource.data.userId;
        }
      }
    }
    """)

def main():
    """Main function to set up all collections"""
    print("🚀 Setting up Firestore collections for SafeYouth AI...")
    print("=" * 50)
    
    try:
        create_users_collection()
        print("-" * 30)
        
        create_mood_logs()
        print("-" * 30)
        
        create_opportunities()
        print("-" * 30)
        
        create_learning_modules()
        print("-" * 30)
        
        create_drug_hotspots()
        print("-" * 30)
        
        setup_security_rules()
        print("-" * 30)
        
        print("\n✅ Firestore setup completed successfully!")
        print("\n📊 Your collections are now ready with sample data.")
        print("🔗 View them at: https://console.firebase.google.com")
        
    except Exception as e:
        print(f"❌ Error setting up Firestore: {e}")

if __name__ == "__main__":
    main()