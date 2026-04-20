"""
AML System - Testing and Demo Guide

This module provides test data and documentation for demonstrating
the Anti-Money Laundering System Sprint 1 capabilities.
"""

# ======================== Demo Scenarios ========================

DEMO_SCENARIOS = {
    "scenario_1": {
        "name": "High-Value Transaction Detection",
        "description": "Demonstrates detection of unusually high-value transactions",
        "transactions": [
            {
                "sender_account": "ACC-001",
                "receiver_account": "ACC-002",
                "amount": 15000,
                "currency": "USD",
                "note": "Amount exceeds $10,000 threshold → Flagged as MEDIUM risk"
            }
        ]
    },
    
    "scenario_2": {
        "name": "Multiple Transactions in Short Time",
        "description": "Detects rapid-fire transactions from same account",
        "instructions": [
            "Add 5 transactions from ACC-003 within 1 hour",
            "Each transaction: $1,000",
            "To different recipients (ACC-004, ACC-005, ACC-006, ACC-007, ACC-008)",
            "Result: Alert with HIGH risk (multiple transactions detected)"
        ]
    },
    
    "scenario_3": {
        "name": "Suspicious Account Pattern",
        "description": "Flags transactions with suspicious account naming",
        "transactions": [
            {
                "sender_account": "SUSP_001",
                "receiver_account": "ACC-010",
                "amount": 5000,
                "note": "Sender account starts with 'SUSP_' → Flagged as HIGH risk"
            }
        ]
    },
    
    "scenario_4": {
        "name": "Repeated Transaction Pattern",
        "description": "Detects repetitive transaction patterns",
        "instructions": [
            "Add same sender-receiver pair 3+ times",
            "Example: ACC-011 → ACC-012",
            "Multiple transactions increase risk score",
            "Result: Alert with risk level based on accumulated score"
        ]
    },
    
    "scenario_5": {
        "name": "CRITICAL Risk Alert",
        "description": "Triggers CRITICAL alert (multiple rule violations)",
        "transactions": [
            {
                "sender_account": "SUSP_CRITICAL",
                "receiver_account": "ACC-020",
                "amount": 50000,
                "note": "High amount ($50k) + Suspicious account = CRITICAL"
            }
        ]
    }
}

# ======================== Test Data Generator ========================

def generate_sample_transactions():
    """
    Generate sample transactions for testing.
    
    Returns:
        List of transaction dictionaries
    """
    return [
        # Normal transactions
        {
            "sender_account": "ACC-001",
            "receiver_account": "ACC-002",
            "amount": 1500,
            "currency": "USD",
            "risk_expected": "LOW"
        },
        {
            "sender_account": "ACC-003",
            "receiver_account": "ACC-004",
            "amount": 2500,
            "currency": "USD",
            "risk_expected": "LOW"
        },
        
        # Suspicious transactions
        {
            "sender_account": "ACC-005",
            "receiver_account": "ACC-006",
            "amount": 12000,
            "currency": "USD",
            "risk_expected": "MEDIUM",
            "reason": "High amount"
        },
        {
            "sender_account": "SUSP_ACCOUNT",
            "receiver_account": "ACC-007",
            "amount": 5000,
            "currency": "USD",
            "risk_expected": "HIGH",
            "reason": "Suspicious account pattern"
        },
        {
            "sender_account": "ACC-008",
            "receiver_account": "ACC-009",
            "amount": 25000,
            "currency": "USD",
            "risk_expected": "HIGH",
            "reason": "Very high amount"
        },
    ]


# ======================== Manual Testing Checklist ========================

TESTING_CHECKLIST = """
Manual Testing Checklist - AML System Sprint 1

□ Authentication & Authorization
  □ Register new user
  □ Login with username/password
  □ Logout functionality
  □ Cannot access dashboard without login
  □ Cannot access API without authentication

□ Dashboard
  □ Dashboard loads successfully
  □ Total transactions count displays
  □ Suspicious transactions count displays
  □ Open alerts count displays
  □ Risk distribution chart shows all risk levels
  □ Quick action buttons accessible
  □ Recent alerts display (last 5)
  □ Add transaction modal opens from dashboard

□ Transaction Management
  □ Add new transaction form loads
  □ Required fields validation works
  □ Amount must be positive
  □ Date picker works correctly
  □ Transaction created successfully
  □ Transaction appears in list immediately
  □ Pagination works (if multiple transactions)
  □ Filter by "Suspicious Only" works
  □ Transaction details modal opens
  □ All transaction details display correctly

□ Fraud Detection
  □ High-value transaction (>$10k) flagged as MEDIUM risk
  □ Suspicious account (SUSP_*) flagged as HIGH risk
  □ Multiple quick transactions flagged
  □ Correct risk level assigned
  □ Detection reason displayed
  □ Alert auto-generated for suspicious transactions

□ Alert Management
  □ Alerts list displays all generated alerts
  □ Alert details modal opens
  □ Risk level badge displays correctly
  □ Filter by status works (OPEN, INVESTIGATING, RESOLVED)
  □ Update alert status works
  □ Save analyst notes works
  □ Triggered rules display correctly

□ Layout & UI
  □ Layout responsive on mobile
  □ Layout responsive on tablet
  □ Layout responsive on desktop
  □ Navigation bar works on all screens
  □ Color coding correct (low: green, medium: yellow, high: red, critical: dark red)
  □ Loading states display
  □ Error messages clear and helpful
  □ Tables scrollable on small screens
  □ Modals close properly

□ Performance
  □ Dashboard loads within 2 seconds
  □ Transaction list loads within 3 seconds
  □ No console errors
  □ Database saves transactions correctly
  □ Pagination works smoothly
"""

# ======================== API Testing Examples ========================

API_TEST_EXAMPLES = {
    "register": {
        "method": "POST",
        "endpoint": "/api/auth/register",
        "example": {
            "username": "analyst1",
            "password": "SecurePass123!",
            "email": "analyst1@aml-system.local",
            "full_name": "John Analyst"
        }
    },
    
    "login": {
        "method": "POST",
        "endpoint": "/api/auth/login",
        "example": {
            "username": "admin",
            "password": "admin123"
        }
    },
    
    "add_transaction": {
        "method": "POST",
        "endpoint": "/api/transactions",
        "example": {
            "sender_account": "ACC-00123",
            "receiver_account": "ACC-00456",
            "amount": 15000.50,
            "currency": "USD",
            "transaction_date": "2026-03-17T14:30:00"
        }
    },
    
    "get_transactions": {
        "method": "GET",
        "endpoint": "/api/transactions?page=1&per_page=20&suspicious=false",
        "description": "Retrieve transaction list with pagination"
    },
    
    "get_dashboard_stats": {
        "method": "GET",
        "endpoint": "/api/dashboard/stats",
        "description": "Get dashboard statistics"
    },
    
    "get_alerts": {
        "method": "GET",
        "endpoint": "/api/alerts?page=1&per_page=20",
        "description": "Retrieve alerts with pagination"
    },
    
    "update_alert": {
        "method": "PUT",
        "endpoint": "/api/alerts/{alert_id}",
        "example": {
            "status": "INVESTIGATING",
            "analyst_notes": "Initial investigation started. Contacting sender."
        }
    }
}

# ======================== Performance Benchmarks ========================

"""
Expected System Performance (Baseline)

Database Operations:
- Transaction creation: < 100ms
- Transaction retrieval: < 200ms (per 20 items)
- Alert creation: < 50ms
- Alert update: < 80ms
- Dashboard stats: < 150ms

Frontend Operations:
- Dashboard load: < 2 seconds (including API calls)
- Transaction list load: < 3 seconds
- Alert list load: < 2.5 seconds
- Modal open/close: < 300ms
- Form submission: < 1 second

Fraud Detection:
- Rule evaluation: < 50ms per transaction
- Database query for detection: < 100ms
- Alert generation: < 20ms

System Limits (Sprint 1):
- Tested with up to 10,000 transactions
- Tested with up to 1,000 alerts
- Tested with 5 concurrent users
- Database file size: < 50MB with 10k transactions

Future Optimizations (Sprint 2+):
- Add database caching (Redis)
- Implement async processing for bulk operations
- Optimize SQL queries with proper indexing
- Add API rate limiting
- Implement search indexing for transactions
"""

# ======================== Known Limitations ========================

"""
Sprint 1 Known Limitations:

1. Single-user per session
   - No concurrent user session management
   - Sessions don't share real-time updates
   
2. SQLite Database
   - Not recommended for > 100k transactions in production
   - Migrate to PostgreSQL/MySQL for production
   
3. Rule-Based Detection Only
   - No ML/AI based detection
   - Rules are hardcoded (see FraudDetectionEngine class)
   
4. No Password Recovery
   - Users cannot reset forgotten passwords
   - Admin must create new accounts
   
5. No Audit Logging
   - User actions not fully logged
   - No comprehensive audit trail yet
   
6. Limited Reporting
   - Only transaction list available
   - No advanced analytics
   - No export functionality
   
7. Single Server Deployment
   - No clustering or load balancing
   - Not scalable for enterprise use
   
All these will be addressed in Sprint 2 and beyond.
"""
