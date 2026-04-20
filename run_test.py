"""
Run AML System in Test Mode with Dummy Data

This script automatically seeds the database with test data and starts the application.
Perfect for demos and testing all system features.
"""

import os
import sys
from datetime import datetime
from app import app, db, User, Transaction, Alert
from seed_data import generate_dummy_data, DUMMY_USERS
import random
import json

def setup_test_environment():
    """Set up test database with dummy data"""
    print("\n" + "="*60)
    print("🧪 AML SYSTEM - TEST ENVIRONMENT SETUP")
    print("="*60)
    
    with app.app_context():
        # Create all tables
        print("\n📦 Creating database tables...")
        db.create_all()
        print("   ✅ Tables created")
        
        # Clear existing data
        print("\n🗑️  Clearing any existing test data...")
        Alert.query.delete()
        Transaction.query.delete()
        User.query.delete()
        db.session.commit()
        print("   ✅ Database cleared")
        
        # Create test users
        print("\n👥 Creating test users...")
        for user_data in DUMMY_USERS:
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                full_name=user_data['full_name'],
                role=user_data['role']
            )
            user.set_password(user_data['password'])
            db.session.add(user)
        
        # Create admin user
        admin = User(
            username='admin',
            email='admin@aml-system.local',
            full_name='System Administrator',
            role='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print(f"   ✅ Created {len(DUMMY_USERS) + 1} test users")
        
        # Generate and add dummy transactions
        print("\n💰 Generating 150 dummy transactions...")
        transactions_data = generate_dummy_data(150)
        
        for idx, txn_data in enumerate(transactions_data, 1):
            if idx % 30 == 0:
                print(f"   Processing: {idx}/{len(transactions_data)}")
            
            transaction = Transaction(
                transaction_id=txn_data['transaction_id'],
                sender_account=txn_data['sender_account'],
                receiver_account=txn_data['receiver_account'],
                amount=txn_data['amount'],
                currency=txn_data['currency'],
                transaction_date=txn_data['transaction_date'],
                is_suspicious=txn_data['is_suspicious'],
                risk_level=txn_data['risk_level'],
                detection_reason=txn_data.get('detection_reason', None)
            )
            db.session.add(transaction)
            db.session.flush()
            
            # Create alert if suspicious
            if txn_data['is_suspicious']:
                analyst_notes = None
                if random.random() < 0.3:
                    analyst_notes = random.choice([
                        'Initial investigation started',
                        'Awaiting customer verification',
                        'Documents requested from sender',
                        'Cross-referencing with watchlist',
                        'Following up on compliance check'
                    ])
                
                alert = Alert(
                    transaction_id=transaction.id,
                    risk_level=txn_data['risk_level'],
                    status=random.choice(['OPEN', 'INVESTIGATING', 'OPEN', 'OPEN']),
                    triggered_rules=txn_data.get('triggered_rules', '[]'),
                    analyst_notes=analyst_notes
                )
                db.session.add(alert)
        
        db.session.commit()
        print(f"   ✅ Created {len(transactions_data)} transactions")
        
        # Print statistics
        print("\n" + "="*60)
        print("📊 DATABASE STATISTICS")
        print("="*60)
        
        total_users = User.query.count()
        total_txns = Transaction.query.count()
        suspicious_txns = Transaction.query.filter_by(is_suspicious=True).count()
        total_alerts = Alert.query.count()
        
        print(f"Users:                    {total_users}")
        print(f"Total Transactions:       {total_txns}")
        print(f"Suspicious Transactions:  {suspicious_txns}")
        print(f"Suspicious Rate:          {(suspicious_txns/total_txns*100):.1f}%")
        print(f"Total Alerts:             {total_alerts}")
        
        # Risk distribution
        risk_dist = db.session.query(
            Transaction.risk_level,
            db.func.count(Transaction.id).label('count')
        ).group_by(Transaction.risk_level).all()
        
        if risk_dist:
            print("\nRisk Distribution:")
            for risk, count in sorted(risk_dist, key=lambda x: ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'].index(x[0])):
                pct = (count / total_txns * 100)
                print(f"  {risk:<10} {count:>4} ({pct:>5.1f}%)")
        
        print("\n" + "="*60)
        print("🔐 TEST CREDENTIALS")
        print("="*60)
        print("\nAdmin Account:")
        print("  Username: admin")
        print("  Password: admin123")
        print("\nTest Analyst Accounts:")
        for user in DUMMY_USERS[:3]:
            print(f"  {user['username']:<20} / {user['password']}")
        
        print("\n" + "="*60)
        print("✅ TEST ENVIRONMENT READY!")
        print("="*60)
        print("\n🚀 Starting Flask application on http://localhost:5000")
        print("   Press Ctrl+C to stop the server\n")


if __name__ == '__main__':
    try:
        setup_test_environment()
        
        # Start Flask app
        app.run(
            debug=True,
            host='0.0.0.0',
            port=5000,
            use_reloader=True
        )
    except KeyboardInterrupt:
        print("\n\n⛔ Server stopped")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)
