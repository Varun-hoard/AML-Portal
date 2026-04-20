# AML System - Commands Reference Guide

## 🚀 Quick Start Commands

### Fastest Way to Start
```bash
python run_test.py
```
✨ **Loads app with 150 sample transactions automatically**

---

### Interactive Menu (Easiest!)

**Windows:**
```bash
run_test.bat
```

**Mac/Linux:**
```bash
bash run_test.sh
```

Then select from interactive menu.

---

## 📋 CLI Management Commands

All commands use: `python manage.py [command] [options]`

### 1. Seed Database with Dummy Data
```bash
python manage.py seed-db --count 100 --users 5
```

**Options:**
- `--count` (default: 100) - Number of transactions
- `--users` (default: 5) - Number of test users

**What it does:**
- Creates database tables
- Adds 5+ test users with credentials
- Generates N transactions with realistic patterns
- Creates alerts for suspicious transactions
- Prints statistics and credentials

**Output Example:**
```
🌱 Seeding database...
✅ Tables created
👥 Creating 5 test users...
✅ Created 5 users
💰 Creating 100 dummy transactions...
✅ Created 100 transactions

📋 Test Credentials:
==================================================
Default Admin:
  Username: admin
  Password: admin123

Other Test Users:
  analyst1        / analyst123
  analyst2        / analyst123
  supervisor      / super123
  ...

📊 Database Statistics:
  Total Transactions: 100
  Suspicious Transactions: 28
  Total Alerts: 28
==================================================
```

---

### 2. Clear All Data
```bash
python manage.py clear-db
```

**⚠️ Warning:** Deletes ALL transactions, alerts, and users

**Confirmation:** You'll be asked to confirm before deletion

**Time:** < 1 second

---

### 3. Reset Database
```bash
python manage.py reset-db
```

**What it does:**
- Drops all tables
- Creates fresh schema
- Creates default admin user (admin/admin123)

**⚠️ Warning:** Deletes everything and starts fresh

**Time:** < 2 seconds

**Use case:** Start completely fresh

---

### 4. View Database Statistics
```bash
python manage.py show-stats
```

**Displays:**
- User count
- Total transactions
- Suspicious transactions
- Alert count
- Suspicious rate (percentage)
- Risk distribution (LOW/MEDIUM/HIGH/CRITICAL)

**Output Example:**
```
📊 Database Statistics:
────────────────────────────────────────
Users:                    6
Total Transactions:       100
Suspicious Transactions:  28
Alerts Generated:         28
Suspicious Rate:          28.0%
────────────────────────────────────────

📈 Risk Distribution:
  LOW        66 (66.0%)
  MEDIUM     18 (18.0%)
  HIGH       14 (14.0%)
  CRITICAL    2 (2.0%)
```

---

### 5. Show All Users
```bash
python manage.py show-users
```

**Displays:**
- Username
- Email
- Role
- Default credentials

**Output Example:**
```
👥 Users in Database:
────────────────────────────────────────────────────────────────────
Username             Email                          Role      
────────────────────────────────────────────────────────────────────
admin                admin@aml-system.local         admin
analyst1             analyst1@aml-system.local      analyst
analyst2             analyst2@aml-system.local      analyst
supervisor           supervisor@aml-system.local    analyst
────────────────────────────────────────────────────────────────────

📋 Default Credentials:
Username: admin
Password: admin123
```

---

### 6. Show Recent Alerts
```bash
python manage.py show-alerts --limit 10
```

**Options:**
- `--limit` (default: 10) - Number of alerts to display

**Displays:**
- Alert ID
- Transaction details
- Sender/Receiver
- Risk level
- Status
- Date created

**Output Example:**
```
🚨 Recent Alerts (Last 3):
────────────────────────────────────────────────────────────────────

Alert #1
  Transaction ID: TXN-1710699000-45AB
  Amount: $25,678.50
  Sender → Receiver: ACC-45123 → ACC-67890
  Risk Level: HIGH
  Status: OPEN
  Date: 2026-03-17 14:30:00

Alert #2
  Transaction ID: TXN-1710698500-12BC
  Amount: $5,432.10
  Sender → Receiver: SUSP_ACCOUNT → ACC-98765
  Risk Level: HIGH
  Status: INVESTIGATING
  Date: 2026-03-17 14:15:00

...
```

---

### 7. Run & Seed Test Data
```bash
python manage.py run-test --count 100 --mode test
```

**Options:**
- `--count` (default: 100) - Number of transactions
- `--mode` (default: test) - "test" or "prod"

**Test Mode:**
- Disables HTTPS requirement
- Sets debug=True
- Enables hot-reload
- Perfect for development

**Production Mode:**
- Sets debug=False
- Requires proper configuration
- For deployment

---

## 🎯 Scenario-Based Commands

### Scenario 1: Quick Demo to Stakeholders
```bash
# 1. Reset database
python manage.py reset-db

# 2. Load large dataset
python manage.py seed-db --count 200

# 3. Show statistics
python manage.py show-stats

# 4. Start app
python run_test.py

# 5. Demo features (15-20 min)
# 6. Show dashboard, create transactions, review alerts
```

**Time:** ~30 seconds setup + demo time

---

### Scenario 2: Developer Testing
```bash
# Start with fresh data
python run_test.py

# Test throughout the day

# Clear when switching to next test
python manage.py clear-db
```

**Repeat as needed**

---

### Scenario 3: Performance Testing
```bash
# Light load (100 transactions)
python manage.py seed-db --count 100
python app.py

# Medium load (500 transactions)
python manage.py reset-db
python manage.py seed-db --count 500
python app.py

# Heavy load (1000 transactions)
python manage.py reset-db
python manage.py seed-db --count 1000
python app.py
```

---

### Scenario 4: End-to-End Testing
```bash
# 1. Start fresh
python manage.py reset-db

# 2. Load test data
python manage.py seed-db --count 150

# 3. Verify data
python manage.py show-stats

# 4. Start app
python app.py

# 5. In browser:
#    - Login with admin/admin123
#    - Review dashboard
#    - Check transactions
#    - Review alerts
#    - Update alert status

# 6. Cleanup
python manage.py clear-db
```

---

### Scenario 5: Switching Between Environments

**Development (with test data):**
```bash
python run_test.py
```

**Staging (fresh):**
```bash
python manage.py reset-db
python app.py
```

**Production (no test data):**
```bash
python manage.py clear-db
python app.py
```

---

## 🔄 Command Sequences

### Fresh Start Sequence
```bash
python manage.py reset-db              # Start fresh
python manage.py seed-db --count 150   # Load data
python manage.py show-stats            # Verify
python app.py                          # Run app
```

### Keep Current Data Sequence
```bash
python manage.py show-stats            # Check current
# ... use the app with existing data ...
python app.py                          # Start app
```

### Data Management Sequence
```bash
python manage.py show-users            # See users
python manage.py show-alerts           # See alerts
python manage.py show-stats            # See stats
python manage.py clear-db              # Clear if needed
```

---

## 🐛 Troubleshooting Commands

### Issue: Database locked
```bash
# Solution: Reset completely
python manage.py reset-db
python manage.py seed-db --count 100
python run_test.py
```

### Issue: Want to see current state
```bash
python manage.py show-stats
python manage.py show-users
python manage.py show-alerts --limit 20
```

### Issue: Accidental data loss
```bash
# Restore from backup (if you have one)
cp aml_system.db.backup aml_system.db

# Or recreate from scratch
python manage.py seed-db --count 150
```

### Issue: Wrong number of tests
```bash
# Clear and reload with new amount
python manage.py clear-db
python manage.py seed-db --count 200
```

---

## ⚙️ Production Commands

### Setup Production
```bash
# Clean database
python manage.py reset-db

# Verify it's clean
python manage.py show-stats

# Change password in app.py init_db() function

# Deploy app
python app.py
```

### Backup Before Production
```bash
# Create backup
cp aml_system.db aml_system.db.prod.backup

# View what you're protecting
python manage.py show-stats
```

### Restore Production Backup
```bash
cp aml_system.db.prod.backup aml_system.db
python manage.py show-stats
```

---

## 📊 Data Generation Reference

### Small Dataset (50 transactions)
```bash
python manage.py seed-db --count 50
```
- Size: ~200KB
- Suspicious: 12-17
- Load time: < 1 second

### Medium Dataset (150 transactions)
```bash
python manage.py seed-db --count 150
```
- Size: ~500KB
- Suspicious: 40-45
- Load time: ~1.5 seconds
- **Recommended for demos**

### Large Dataset (500 transactions)
```bash
python manage.py seed-db --count 500
```
- Size: ~2MB
- Suspicious: 120-160
- Load time: ~2 seconds
- Good for performance testing

### Heavy Dataset (1000 transactions)
```bash
python manage.py seed-db --count 1000
```
- Size: ~4MB
- Suspicious: 250-350
- Load time: ~2.5 seconds
- Consider PostgreSQL for production volume

---

## 🔒 Security Reminders

When using `seed-db` or `run-test`:
1. ⚠️ Test data only - NOT for production
2. ⚠️ Default passwords are weak
3. ✅ Use `clear-db` before going live
4. ✅ Change default admin password
5. ✅ Use strong SECRET_KEY in production

---

## 📞 Help & Support

### Get Help on Any Command
```bash
python manage.py seed-db --help
python manage.py clear-db --help
python manage.py show-stats --help
```

### Documentation Files
- [README.md](README.md) - Full setup & features
- [QUICK_START.md](QUICK_START.md) - 5-minute setup
- [TEST_ENVIRONMENT.md](TEST_ENVIRONMENT.md) - Test data details
- [TESTING_GUIDE.md](TESTING_GUIDE.md) - Manual testing checklist

### Common Issues
- Check TEST_ENVIRONMENT.md "Troubleshooting" section
- Review console output for error messages
- Use `show-stats` to verify database state

---

## ✅ Command Checklist

Essential commands to remember:

- [ ] `python run_test.py` - Quick start with data
- [ ] `python manage.py seed-db --count 100` - Load specific amount
- [ ] `python manage.py show-stats` - Check database
- [ ] `python manage.py clear-db` - Clean database
- [ ] `python manage.py reset-db` - Fresh start
- [ ] `python app.py` - Start application

---

**Happy Testing! 🎉**

For detailed information, see TEST_ENVIRONMENT.md
