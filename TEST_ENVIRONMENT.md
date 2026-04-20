# AML System - Test Environment & Dummy Data Guide

## 🧪 Quick Test Setup

### Option 1: Instant Test (Recommended)
Run with dummy data loaded automatically:

```bash
python run_test.py
```

This will:
- ✅ Create fresh database
- ✅ Load 150 sample transactions
- ✅ Generate alerts for suspicious transactions
- ✅ Start the Flask app immediately
- 🔐 Login with: `admin` / `admin123`

**Time to running: ~10 seconds** ⚡

---

### Option 2: Use Management CLI

#### Install First
```bash
pip install -r requirements.txt
```

#### Seed Database with Dummy Data
```bash
python manage.py seed-db --count 100 --users 5
```

Options:
- `--count` (default: 100) - Number of transactions to generate
- `--users` (default: 5) - Number of test user accounts to create

Output will show:
- Created users with credentials
- Database statistics
- Login credentials

#### Clear All Data
```bash
python manage.py clear-db
```

⚠️ **Warning**: This deletes ALL transactions, alerts, and users. You'll be asked to confirm.

#### Reset Database (Clean Slate)
```bash
python manage.py reset-db
```

This:
- Deletes all data
- Recreates database schema
- Creates default admin account

#### Display Statistics
```bash
python manage.py show-stats
```

Shows:
- User count
- Total transactions
- Suspicious transactions
- Alert count
- Risk distribution

#### Show All Users
```bash
python manage.py show-users
```

Lists all users with their roles and emails.

#### Show Recent Alerts
```bash
python manage.py show-alerts --limit 15
```

Options:
- `--limit` (default: 10) - Number of alerts to display

---

## 📊 Test Data Architecture

### Transaction Distribution

The dummy data generator creates realistic transaction patterns:

| Type | Amount Range | Probability | Risk Level |
|------|-------------|-------------|-----------|
| Normal Transfer | $500-5k | 65% | LOW |
| Medium Transfer | $5k-10k | 20% | LOW |
| High Value | $10k-50k | 5% | MEDIUM |
| Critical Value | $50k-200k | 2% | HIGH |
| Rapid Small | $100-2k | 8% | LOW |

### Fraud Distribution

With 150 transactions:
- **~40-50 suspicious** transactions (27-33%)
- **40-50 alerts** generated

Risk breakdown:
- **LOW**: 100-110 transactions (67-73%)
- **MEDIUM**: 20-30 transactions (13-20%)
- **HIGH**: 15-25 transactions (10-17%)
- **CRITICAL**: 2-5 transactions (1-3%)

---

## 🧬 Triggered Rules in Test Data

### Rule 1: High Amount (>$10,000)
```
✓ Automatically detected and flagged
✓ Triggers MEDIUM/HIGH risk
```

Example transactions:
- ACC-45123 → ACC-67890: $15,000
- ACC-12345 → ACC-98765: $45,000

### Rule 2: Multiple Transactions (5+ in 60 min)
```
✓ Generator simulates rapid transactions
✓ Flags after 5th transaction
✓ Risk escalates with volume
```

### Rule 3: Repeated Pattern (Same sender-receiver 3+ times)
```
✓ Detects repetitive pairs
✓ Increases risk with each repeat
```

### Rule 4: Suspicious Accounts (Starts with SUSP_)
```
✓ 5% of senders have suspicious prefix
✓ 3% of receivers have suspicious prefix
✓ Always triggers HIGH risk
```

---

## 📋 Test Scenarios

### Scenario 1: New Analyst Onboarding
1. Load dummy data: `python run_test.py`
2. Login as: `analyst1` / `analyst123`
3. Navigate to Dashboard
4. Review suspicious transactions
5. Update alert status and add notes

### Scenario 2: Alert Investigation Flow
1. Load dummy data: `python run_test.py`
2. Go to Alerts tab
3. Filter by "OPEN" status
4. Click on an alert
5. Review transaction details
6. Update status to "INVESTIGATING"
7. Add analyst notes

### Scenario 3: System Training
1. `python manage.py seed-db --count 200`
2. Show stats: `python manage.py show-stats`
3. Show recent alerts: `python manage.py show-alerts --limit 20`
4. Start app: `python app.py`
5. Demo the dashboard and features

### Scenario 4: Fraud Detection Demo
1. Load data: `python run_test.py`
2. Go to Dashboard
3. Click "Add Transaction"
4. Enter high amount: $25,000
5. See it flagged as MEDIUM risk
6. Try SUSP_ACCOUNT as sender
7. See it flagged as HIGH risk
8. Go to Alerts and review generated alert

---

## 🔄 Database Management

### Check Current Database State
```bash
python manage.py show-stats
```

### Switch Between Environments

#### Test Environment
```bash
# With dummy data
python run_test.py

# Or manually
python manage.py reset-db
python manage.py seed-db --count 150
python app.py
```

#### Production Environment
```bash
# Without test data
python manage.py reset-db
python app.py
```

### Backup Test Data
```bash
# Copy the database file
cp aml_system.db aml_system.db.backup
```

### Restore from Backup
```bash
# Restore the database
cp aml_system.db.backup aml_system.db
```

---

## 🎯 Using Test Users

### Pre-loaded Test Accounts

| Username | Password | Role | Email |
|----------|----------|------|-------|
| admin | admin123 | admin | admin@aml-system.local |
| analyst1 | analyst123 | analyst | analyst1@aml-system.local |
| analyst2 | analyst123 | analyst | analyst2@aml-system.local |
| supervisor | super123 | analyst | supervisor@aml-system.local |
| compliance | compliance123 | analyst | compliance@aml-system.local |
| manager | manager123 | analyst | manager@aml-system.local |

---

## 📈 Performance with Test Data

### With 150 Transactions
- Dashboard load: ~1.5 seconds
- Transaction list load: ~2 seconds
- Alert list load: ~1.5 seconds
- Add new transaction: ~800ms
- Update alert: ~600ms

### With 500 Transactions
- Dashboard load: ~2 seconds
- Transaction list load: ~2.5 seconds
- Pagination improves performance (20 per page)

### With 1000 Transactions
- Dashboard load: ~2.5 seconds
- Pagination essential
- Still responsive
- Consider moving to PostgreSQL for production

---

## 🔧 Customizing Test Data

### Generate Different Amounts

More transactions (for stress testing):
```bash
python manage.py seed-db --count 500
```

Fewer transactions (for quick testing):
```bash
python manage.py seed-db --count 50
```

### Edit seed_data.py

Modify `TRANSACTION_SCENARIOS` to change:
- Amount ranges
- Probability weights
- Risk levels
- Descriptions

Example - more high-value transactions:
```python
{
    'name': 'High Value Transfer',
    'amount_range': (10000, 50000),
    'suspicious': True,
    'risk': 'MEDIUM',
    'probability': 0.15,  # Increased from 0.05
    'description': 'High transaction amount',
    'triggered_rules': ['High Amount Detected']
}
```

---

## 🐛 Troubleshooting

### Database Already Exists
If you see "database is locked" error:
```bash
# Clear and reset completely
python manage.py reset-db
python manage.py seed-db --count 100
python run_test.py
```

### Port 5000 Already in Use
```bash
# Use different port (edit app.py last line)
app.run(debug=False, host='0.0.0.0', port=5001)
```

### Changes Not Reflecting
```bash
# Clear browser cache
# Press Ctrl+Shift+Delete to open cache settings

# Or restart from scratch
python manage.py reset-db
python run_test.py
```

---

## 📝 Workflow Examples

### Daily Testing Routine

**Morning - Fresh Start**
```bash
python manage.py reset-db
python manage.py seed-db --count 150
python app.py
```

**Throughout Day**
- Test various features
- Add real transactions as needed

**Evening - Cleanup**
```bash
python manage.py clear-db
```

### Demonstration to Stakeholders

```bash
# 1. Reset and seed
python manage.py reset-db
python manage.py seed-db --count 200

# 2. Show stats
python manage.py show-stats

# 3. Start app
python run_test.py

# 4. Demo features (15-20 minutes)

# 5. Logout and restart
# Repeat step 2-4 for another demo
```

---

## 🔐 Security Notes

- ⚠️ Test data is **NOT** for production
- ⚠️ Default passwords are **weak** - change them
- ⚠️ Test accounts have full permissions
- ⚠️ Database files are **not encrypted**
- ✅ Use `python manage.py clear-db` when testing sensitive features

---

## 📚 Additional Commands

### Check Database File Size
```bash
# Windows
dir *.db

# Mac/Linux
ls -lh *.db
```

### View Raw Database (SQLite)
```bash
sqlite3 aml_system.db
```

### Export Transactions to CSV (Advanced)
```python
# Create a script to export data
import pandas as pd
from app import Transaction, app

with app.app_context():
    txns = Transaction.query.all()
    df = pd.DataFrame([
        {
            'ID': t.transaction_id,
            'Sender': t.sender_account,
            'Receiver': t.receiver_account,
            'Amount': t.amount,
            'Suspicious': t.is_suspicious,
            'Risk': t.risk_level,
            'Date': t.transaction_date
        }
        for t in txns
    ])
    df.to_csv('transactions_export.csv', index=False)
    print(f"Exported {len(df)} transactions")
```

---

## ✅ Checklist for Testing

- [ ] Reset database
- [ ] Seed with dummy data
- [ ] Check dashboard loads
- [ ] View transactions list
- [ ] Review alerts
- [ ] Add new transaction
- [ ] Update alert status
- [ ] Check statistics
- [ ] Test filtering
- [ ] Test pagination
- [ ] Clear database

---

## 🎓 Learning Path

1. **Understand the System**
   - Read README.md
   - Review app.py architecture

2. **Create Test Environment**
   - `python run_test.py`
   - Explore the interface

3. **Analyze Test Data**
   - `python manage.py show-stats`
   - Review transaction patterns

4. **Customize for Your Needs**
   - Modify seed_data.py
   - Add your own rules
   - Test edge cases

5. **Deploy with Confidence**
   - Clear test data
   - Set production configuration
   - Deploy to cloud

---

**Happy Testing! 🎉**

For questions, refer to README.md or QUICK_START.md
