# 🎯 START HERE - AML System Quick Navigation

## What Is This?

An **Anti-Money Laundering (AML) System** that automatically detects suspicious financial transactions using rule-based fraud detection. It includes a modern web interface, REST API, test data generation, and comprehensive documentation.

**Status:** ✅ **Production Ready** - Sprint 1 Complete

---

## ⚡ I'm in a Hurry (2 minute setup)

```bash
python run_test.py
```

Then open browser: **http://localhost:5000**

Login: **admin** / **admin123**

**Done!** You now have a fully working AML system with 150 sample transactions. 🎉

---

## 🗂️ Documentation Hub

Pick what you need based on your role:

### 👨‍💼 **I'm a Manager/Decision Maker**
Start with: **[SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md)** (5 min read)
- What the system does
- How it detects fraud
- Architecture overview
- Key metrics

### 👨‍💻 **I'm a Developer**
Start with: **[QUICKREF.md](QUICKREF.md)** (Print-friendly commands)
Then read: **[SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md)** (Architecture)
Then read: **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** (Code layout)

### 🧪 **I'm a QA/Tester**
Start with: **[QUICKREF.md](QUICKREF.md)** (Quick commands)
Then read: **[TEST_ENVIRONMENT.md](TEST_ENVIRONMENT.md)** (Test data setup)
Then read: **[TESTING_GUIDE.md](TESTING_GUIDE.md)** (Test procedures)

### 🚀 **I'm DevOps/Infrastructure**
Start with: **[QUICK_START.md](QUICK_START.md)** (3 setup paths)
Then read: **[COMMANDS_REFERENCE.md](COMMANDS_REFERENCE.md)** (All CLI commands)
Reference: **[Dockerfile](Dockerfile)** & **[docker-compose.yml](docker-compose.yml)**

### 📊 **I'm an Analyst**
Start with: **[QUICKREF.md](QUICKREF.md)** (How to login)
Then read: **[SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md)** (Detection rules)
Use: **[TESTING_GUIDE.md](TESTING_GUIDE.md)** (Manual testing)

---

## 📚 All Documentation Files

| File | Purpose | Read Time |
|------|---------|-----------|
| **[QUICKREF.md](QUICKREF.md)** 🔥 | Commands, credentials, shortcuts | 5 min |
| **[QUICK_START.md](QUICK_START.md)** | 3 ways to start the system | 5 min |
| **[SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md)** | Architecture, technology stack | 15 min |
| **[TEST_ENVIRONMENT.md](TEST_ENVIRONMENT.md)** | Test data generation | 10 min |
| **[COMMANDS_REFERENCE.md](COMMANDS_REFERENCE.md)** | All CLI commands detailed | 15 min |
| **[TESTING_GUIDE.md](TESTING_GUIDE.md)** | Manual testing procedures | 10 min |
| **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** | Code organization | 10 min |
| **[README.md](README.md)** | Features, API endpoints, full specs | 20 min |

---

## 🎬 Quick Start Paths

### Path 1️⃣: **"Run It NOW" (Fastest)**
```bash
python run_test.py
# Opens http://localhost:5000 with demo data
# Time: ~10 seconds
```

### Path 2️⃣: **"Interactive Menu" (User-Friendly)**
```bash
run_test.bat              # Windows
bash run_test.sh          # Mac/Linux
# Shows 8-option menu
# Time: ~15 seconds
```

### Path 3️⃣: **"Full Setup from Scratch" (Complete Control)**
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python app.py
# Opens http://localhost:5000 with fresh database
# Time: ~2 minutes
```

---

## 🔐 Demo Login Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| Analyst | `analyst1` | `analyst123` |
| Supervisor | `supervisor` | `super123` |

---

## 🎯 Key Features

✅ **Transaction Management** - Add, view, filter transactions  
✅ **Fraud Detection** - 4 rules automatically score risk  
✅ **Alert System** - Suspicious transactions trigger alerts  
✅ **Dashboard** - Real-time statistics and risk distribution  
✅ **API** - 14+ endpoints for programmatic access  
✅ **Test Data** - Generate 150+ realistic transactions instantly  
✅ **CLI Tools** - Database management commands  
✅ **Responsive UI** - Works on desktop, tablet, mobile  

---

## 🔴 Fraud Detection Rules

The system flags transactions as suspicious based on:

1. **High Amount** (>$10,000)
2. **Rapid Transactions** (5+ in 60 minutes)
3. **Repeated Pattern** (Same sender→receiver 3+ times)
4. **Suspicious Accounts** (Account name starts with "SUSP_")

Each rule adds risk points. Total ≥30 = Suspicious ⚠️

---

## 🚨 Troubleshooting: Common Issues

| Problem | Solution |
|---------|----------|
| **"Port 5000 in use"** | `python app.py --port 5001` |
| **"Database locked"** | `rm instance/aml_system.db` & restart |
| **"Import error"** | `pip install -r requirements.txt` |
| **"Login fails"** | `python manage.py reset-db` to reset |

More help? See **[QUICKREF.md](QUICKREF.md)** troubleshooting section.

---

## 🏗️ What's Inside

```
Core Application:
├─ app.py                 - Flask backend (2000 lines)
├─ manage.py              - CLI tool (7 commands)
├─ seed_data.py           - Test data generator
└─ run_test.py            - Auto setup script

Frontend:
├─ templates/             - 7 HTML pages
└─ static/               - CSS styling, JavaScript

Configuration:
├─ requirements.txt       - Python dependencies
├─ Dockerfile            - Container config
└─ docker-compose.yml    - Multi-container setup

Documentation:
├─ README.md             - Full documentation
├─ QUICKREF.md           - Command reference
├─ QUICK_START.md        - Setup guide
├─ SYSTEM_OVERVIEW.md    - Architecture
├─ TEST_ENVIRONMENT.md   - Testing guide
├─ TESTING_GUIDE.md      - Test procedures
└─ PROJECT_STRUCTURE.md  - Code organization
```

---

## ✅ First-Time Checklist

- [ ] Python 3.8+ installed
- [ ] Run `python run_test.py`
- [ ] Open http://localhost:5000
- [ ] Login with `admin / admin123`
- [ ] Click to Dashboard → See statistics
- [ ] Click to Transactions → View sample data
- [ ] Click to Alerts → See flagged transactions
- [ ] Try adding a new transaction

If all checked ✅ → **System is working!** 🎉

---

## 🤔 Frequently Asked Questions

**Q: Is this production-ready?**  
A: Yes! Sprint 1 is complete and production-quality. See [SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md) for deployment options.

**Q: Can I customize the fraud rules?**  
A: Yes! Edit the `FraudDetectionEngine` class in [app.py](app.py).

**Q: How do I generate more test data?**  
A: `python manage.py seed-db --count 500` (adjust count as needed)

**Q: Can I use a different database?**  
A: Yes! Edit `.env` to use PostgreSQL, MySQL, etc. See [QUICK_START.md](QUICK_START.md).

**Q: What's in the next sprint?**  
A: Machine Learning detection, advanced analytics, email notifications. See [README.md](README.md).

**Q: How do I deploy to production?**  
A: Use Docker. See [Dockerfile](Dockerfile) and [docker-compose.yml](docker-compose.yml).

---

## 👥 Need Help?

### By Topic
- **Setup issues?** → [QUICK_START.md](QUICK_START.md)
- **Commands?** → [QUICKREF.md](QUICKREF.md) or [COMMANDS_REFERENCE.md](COMMANDS_REFERENCE.md)
- **Testing?** → [TEST_ENVIRONMENT.md](TEST_ENVIRONMENT.md) or [TESTING_GUIDE.md](TESTING_GUIDE.md)
- **Architecture?** → [SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md) or [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
- **Everything?** → [README.md](README.md)

### Quick Command Help
```bash
# See system version and check
python manage.py --help

# See all available commands
python manage.py --help | grep -A 50 "Commands:"

# View system statistics
python manage.py show-stats
```

---

## 📊 System Stats (with Default Test Data)

- **Transactions:** 150 total
- **Suspicious:** 40-50 (27-30%)
- **Alerts:** Auto-generated for suspicious transactions
- **Users:** 6 test accounts
- **Rules:** 4 fraud detection rules
- **Risk Levels:** LOW, MEDIUM, HIGH, CRITICAL
- **API Endpoints:** 14+ RESTful endpoints
- **Pages:** 4 main pages + login

---

## 🎓 Learning Path

**Beginner (30 min):**
1. Run `python run_test.py`
2. Login and explore dashboard
3. View transactions and alerts
4. Read [QUICKREF.md](QUICKREF.md)

**Intermediate (2 hours):**
1. Read [SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md)
2. Try all CLI commands from [QUICKREF.md](QUICKREF.md)
3. Create test scenarios with different data amounts
4. Add transactions and watch alerts trigger

**Advanced (4 hours):**
1. Study [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
2. Modify fraud rules in [app.py](app.py)
3. Customize test data in [seed_data.py](seed_data.py)
4. Deploy using [Dockerfile](Dockerfile)

---

## 🚀 Next Steps

### **Immediate (Do this now):**
```bash
python run_test.py
# Then explore: http://localhost:5000
```

### **This Hour:**
- Login with demo credentials
- Review dashboard and statistics
- Try adding a new transaction
- Check if alert was auto-generated

### **Today:**
- Read [SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md)
- Try different test data amounts: `python manage.py seed-db --count 500`
- Read [QUICKREF.md](QUICKREF.md) and bookmark it

### **This Week:**
- Read [COMMANDS_REFERENCE.md](COMMANDS_REFERENCE.md)
- Try deploying with Docker
- Customize fraud rules for your needs
- Create custom test data scenarios

---

## 📞 Support Resources

| Resource | Useful For |
|----------|-----------|
| [QUICKREF.md](QUICKREF.md) | Quick lookup of commands and troubleshooting |
| [SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md) | Understanding how the system works |
| [COMMANDS_REFERENCE.md](COMMANDS_REFERENCE.md) | Detailed CLI documentation |
| [TEST_ENVIRONMENT.md](TEST_ENVIRONMENT.md) | Setting up and managing test data |
| [TESTING_GUIDE.md](TESTING_GUIDE.md) | Manual testing procedures |
| [README.md](README.md) | Complete feature list and API documentation |

---

**Welcome to the AML System! 🎉**

**Start here:** `python run_test.py`

**Questions?** Check the [documentation guide](#-documentation-hub) above.

**Ready to build?** See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) and [SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md).

---

*Last Updated: Sprint 1 Complete*  
*Status: ✅ Production Ready*  
*Version: 1.0.0*
