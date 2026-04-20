"""
Dummy Data Generator for AML System Testing

Generates realistic test data to demonstrate system capabilities.
"""

import random
from datetime import datetime, timedelta
import json

# Test user credentials
DUMMY_USERS = [
    {
        'username': 'analyst1',
        'email': 'analyst1@aml-system.local',
        'full_name': 'John Analyst',
        'password': 'analyst123',
        'role': 'analyst'
    },
    {
        'username': 'analyst2',
        'email': 'analyst2@aml-system.local',
        'full_name': 'Sarah Investigator',
        'password': 'analyst123',
        'role': 'analyst'
    },
    {
        'username': 'supervisor',
        'email': 'supervisor@aml-system.local',
        'full_name': 'Mike Supervisor',
        'password': 'super123',
        'role': 'analyst'
    },
    {
        'username': 'compliance',
        'email': 'compliance@aml-system.local',
        'full_name': 'Emma Compliance',
        'password': 'compliance123',
        'role': 'analyst'
    },
    {
        'username': 'manager',
        'email': 'manager@aml-system.local',
        'full_name': 'David Manager',
        'password': 'manager123',
        'role': 'analyst'
    }
]

# Realistic account prefixes for generating account numbers
ACCOUNT_PREFIXES = {
    'normal': ['ACC', 'USR', 'CLI', 'BUS'],
    'suspicious': ['SUSP', 'FRD', 'BLK'],
}

# Transaction scenarios
TRANSACTION_SCENARIOS = [
    # Normal transactions
    {
        'name': 'Normal Transfer',
        'amount_range': (500, 5000),
        'suspicious': False,
        'risk': 'LOW',
        'probability': 0.65,
        'description': 'Regular business transfer'
    },
    
    # Medium value transactions
    {
        'name': 'Medium Transfer',
        'amount_range': (5000, 10000),
        'suspicious': False,
        'risk': 'LOW',
        'probability': 0.20,
        'description': 'Mid-range business transaction'
    },
    
    # High value (triggers rule 1)
    {
        'name': 'High Value Transfer',
        'amount_range': (10000, 50000),
        'suspicious': True,
        'risk': 'MEDIUM',
        'probability': 0.05,
        'description': 'High transaction amount',
        'triggered_rules': ['High Amount Detected']
    },
    
    # Very high value (triggers rule 1 strongly)
    {
        'name': 'Critical Value Transfer',
        'amount_range': (50000, 200000),
        'suspicious': True,
        'risk': 'HIGH',
        'probability': 0.02,
        'description': 'Very high transaction amount',
        'triggered_rules': ['High Amount Detected']
    },
    
    # Small rapid transaction (combined with others triggers rule 2)
    {
        'name': 'Rapid Small Transfer',
        'amount_range': (100, 2000),
        'suspicious': False,
        'risk': 'LOW',
        'probability': 0.08,
        'description': 'Small rapid transfer'
    },
]


def generate_account_number(suspicious=False):
    """Generate a random account number"""
    accounts = ACCOUNT_PREFIXES['suspicious'] if suspicious else ACCOUNT_PREFIXES['normal']
    prefix = random.choice(accounts)
    number = str(random.randint(10000, 99999))
    return f"{prefix}-{number}"


def generate_dummy_data(count=100):
    """
    Generate dummy transaction data for testing.
    
    Args:
        count: Number of transactions to generate
        
    Returns:
        List of transaction dictionaries with all required fields
    """
    transactions = []
    base_date = datetime.utcnow() - timedelta(days=30)
    
    # Track senders for multiple transaction rule
    sender_transactions = {}  # sender -> list of timestamps
    sender_receiver_pairs = {}  # (sender, receiver) -> count
    
    for i in range(count):
        # Choose random scenario based on probability
        scenario = random.choices(
            TRANSACTION_SCENARIOS,
            weights=[s['probability'] for s in TRANSACTION_SCENARIOS],
            k=1
        )[0]
        
        # Generate transaction details
        sender = generate_account_number(
            suspicious=random.random() < 0.05  # 5% chance of suspicious sender
        )
        receiver = generate_account_number(
            suspicious=random.random() < 0.03  # 3% chance of suspicious receiver
        )
        
        amount = random.uniform(scenario['amount_range'][0], scenario['amount_range'][1])
        
        # Generate transaction timestamp within last 30 days
        days_offset = random.randint(0, 29)
        hours_offset = random.randint(0, 23)
        minutes_offset = random.randint(0, 59)
        transaction_date = base_date + timedelta(
            days=days_offset,
            hours=hours_offset,
            minutes=minutes_offset
        )
        
        # Track for multiple transaction detection
        if sender not in sender_transactions:
            sender_transactions[sender] = []
        sender_transactions[sender].append(transaction_date)
        
        # Track sender-receiver pairs
        pair = (sender, receiver)
        if pair not in sender_receiver_pairs:
            sender_receiver_pairs[pair] = 0
        sender_receiver_pairs[pair] += 1
        
        # Determine risk and suspicious status
        is_suspicious = scenario['suspicious']
        risk_level = scenario['risk']
        triggered_rules = []
        detection_reason = scenario['description']
        
        # Apply detection rules
        
        # Rule 1: High amount
        if amount > 10000:
            is_suspicious = True
            risk_level = 'HIGH' if amount > 30000 else 'MEDIUM'
            triggered_rules.append('High Amount Detected')
        
        # Rule 3: Suspicious account pattern
        if sender.startswith('SUSP_') or receiver.startswith('SUSP_'):
            is_suspicious = True
            risk_level = 'HIGH'
            triggered_rules.append('Suspicious Account Pattern')
        
        # Rule 2 & 3: Multiple transactions and patterns (simulated)
        # Check if we have multiple transactions in short window
        recent_times = [t for t in sender_transactions[sender] 
                       if abs((transaction_date - t).total_seconds()) < 3600]
        if len(recent_times) >= 5:
            is_suspicious = True
            risk_level = 'HIGH'
            triggered_rules.append('Multiple Transactions in Short Time')
        
        # Rule 4: Repeated pattern
        if sender_receiver_pairs[pair] >= 3:
            is_suspicious = True
            triggered_rules.append('Repeated Transaction Pattern')
            if risk_level == 'LOW':
                risk_level = 'MEDIUM'
        
        # Determine final risk level based on all triggered rules
        if len(triggered_rules) >= 2:
            risk_level = 'CRITICAL' if len(triggered_rules) >= 3 else 'HIGH'
        
        # Create transaction record
        transaction = {
            'transaction_id': f"TXN-{int(transaction_date.timestamp())}-{sender[-4:]}",
            'sender_account': sender,
            'receiver_account': receiver,
            'amount': round(amount, 2),
            'currency': random.choice(['USD', 'EUR', 'GBP']),
            'transaction_date': transaction_date,
            'is_suspicious': is_suspicious,
            'risk_level': risk_level,
            'detection_reason': ' | '.join(triggered_rules) if triggered_rules else None,
            'triggered_rules': json.dumps(triggered_rules),
            'analyst_notes': None
        }
        
        transactions.append(transaction)
    
    return transactions


def generate_suspicious_scenarios(count=20):
    """
    Generate specific suspicious transaction scenarios for demonstration.
    
    Args:
        count: Number of special scenarios to generate
        
    Returns:
        List of transaction dictionaries
    """
    transactions = []
    base_date = datetime.utcnow() - timedelta(days=7)
    
    # Scenario 1: High value transaction
    for i in range(3):
        transactions.append({
            'transaction_id': f"DEMO-HIGH-{i+1}",
            'sender_account': f"ACC-{random.randint(10000, 99999)}",
            'receiver_account': f"ACC-{random.randint(10000, 99999)}",
            'amount': random.uniform(15000, 50000),
            'currency': 'USD',
            'transaction_date': base_date + timedelta(hours=i),
            'is_suspicious': True,
            'risk_level': 'MEDIUM',
            'detection_reason': 'High Amount Detected',
            'triggered_rules': '["High Amount Detected"]'
        })
    
    # Scenario 2: Suspicious account pattern
    susp_sender = "SUSP_ACCOUNT_001"
    for i in range(3):
        transactions.append({
            'transaction_id': f"DEMO-SUSP-{i+1}",
            'sender_account': susp_sender,
            'receiver_account': f"ACC-{random.randint(10000, 99999)}",
            'amount': random.uniform(3000, 8000),
            'currency': 'USD',
            'transaction_date': base_date + timedelta(hours=5+i),
            'is_suspicious': True,
            'risk_level': 'HIGH',
            'detection_reason': 'Suspicious Account Pattern Detected',
            'triggered_rules': '["Suspicious Account Pattern"]'
        })
    
    # Scenario 3: Multiple rapid transactions (same sender)
    rapid_sender = f"ACC-{random.randint(10000, 99999)}"
    for i in range(6):
        transactions.append({
            'transaction_id': f"DEMO-RAPID-{i+1}",
            'sender_account': rapid_sender,
            'receiver_account': f"ACC-{random.randint(10000, 99999)}",
            'amount': random.uniform(1000, 3000),
            'currency': 'USD',
            'transaction_date': base_date + timedelta(hours=10, minutes=i*5),
            'is_suspicious': True if i >= 4 else False,
            'risk_level': 'HIGH' if i >= 4 else 'LOW',
            'detection_reason': 'Multiple Transactions Detected' if i >= 4 else None,
            'triggered_rules': '["Multiple Transactions in Short Time"]' if i >= 4 else '[]'
        })
    
    # Scenario 4: Repeated pattern (same sender-receiver)
    pattern_sender = f"ACC-{random.randint(10000, 99999)}"
    pattern_receiver = f"ACC-{random.randint(10000, 99999)}"
    
    for i in range(5):
        transactions.append({
            'transaction_id': f"DEMO-PATTERN-{i+1}",
            'sender_account': pattern_sender,
            'receiver_account': pattern_receiver,
            'amount': 5000,
            'currency': 'USD',
            'transaction_date': base_date + timedelta(days=1, hours=i*2),
            'is_suspicious': True if i >= 2 else False,
            'risk_level': 'MEDIUM' if i >= 2 else 'LOW',
            'detection_reason': 'Repeated Transaction Pattern' if i >= 2 else None,
            'triggered_rules': '["Repeated Transaction Pattern"]' if i >= 2 else '[]'
        })
    
    # Scenario 5: Combined rule violations (CRITICAL)
    transactions.append({
        'transaction_id': 'DEMO-CRITICAL-001',
        'sender_account': 'SUSP_CRITICAL',
        'receiver_account': f"ACC-{random.randint(10000, 99999)}",
        'amount': 75000,
        'currency': 'USD',
        'transaction_date': base_date + timedelta(days=2),
        'is_suspicious': True,
        'risk_level': 'CRITICAL',
        'detection_reason': 'Multiple rule violations: High Amount + Suspicious Account',
        'triggered_rules': '["High Amount Detected", "Suspicious Account Pattern"]'
    })
    
    return transactions


if __name__ == '__main__':
    # Test the generator
    data = generate_dummy_data(10)
    for i, txn in enumerate(data, 1):
        print(f"\n{i}. {txn['transaction_id']}")
        print(f"   {txn['sender_account']} → {txn['receiver_account']}")
        print(f"   Amount: ${txn['amount']:,.2f} | Risk: {txn['risk_level']}")
        print(f"   Suspicious: {txn['is_suspicious']}")
        if txn['detection_reason']:
            print(f"   Reason: {txn['detection_reason']}")
