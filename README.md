# AML System - Sprint 1 Configuration Guide

> 🎯 **NEW USER?** Start with **[START_HERE.md](START_HERE.md)** for navigation guide!  
> ⚡ **In a hurry?** Check **[QUICKREF.md](QUICKREF.md)** for commands and quick reference!

## ⚡ Quick Test Setup (RECOMMENDED!)

Want to see the system in action with real data immediately?

```bash
python run_test.py
```

This automatically:
- ✅ Creates database
- ✅ Loads 150 sample transactions
- ✅ Generates suspicious alerts
- ✅ Starts the Flask app
- 🔐 Login: `admin` / `admin123`

**Time to running: ~10 seconds** 🚀

---

## 🎯 Other Quick Options

### Windows Interactive Menu
```bash
run_test.bat
```

### Mac/Linux Interactive Menu
```bash
bash run_test.sh
```

### CLI Commands
```bash
# Seed database with 100 transactions
python manage.py seed-db --count 100

# View statistics
python manage.py show-stats

# Reset database
python manage.py reset-db

# Clear all data
python manage.py clear-db
```

**Full command reference: See [COMMANDS_REFERENCE.md](COMMANDS_REFERENCE.md)**

---

## 📊 Test Environment & Dummy Data

The system includes comprehensive test data generation tools:

### What You Get with `python run_test.py`
- **150 realistic transactions** with various patterns
- **40-50 suspicious transactions** triggering alerts
- **4 fraud detection rules** demonstrated
- **6 test user accounts** with different roles
- **Risk distribution**: LOW (70%), MEDIUM (15%), HIGH (15%)

### Managing Test Data
- **Load data**: `python manage.py seed-db --count 100`
- **View stats**: `python manage.py show-stats`
- **Clear data**: `python manage.py clear-db`
- **See users**: `python manage.py show-users`
- **See alerts**: `python manage.py show-alerts --limit 20`

### Test Scenarios Included
1. High-value transactions (> $10,000)
2. Suspicious account patterns
3. Rapid multiple transactions
4. Repeated transaction patterns
5. Combined rule violations

**Detailed guide: See [TEST_ENVIRONMENT.md](TEST_ENVIRONMENT.md)**

---

## 🛠️ CLI Management Tools

The system includes a powerful CLI for managing test environments and databases:

```bash
# Seed database with 100 transactions (configurable)
python manage.py seed-db --count 100

# Clear all transactions and alerts
python manage.py clear-db

# Reset database completely (drops and recreates)
python manage.py reset-db

# View statistics and risk distribution
python manage.py show-stats

# List all users
python manage.py show-users

# List all alerts with optional filtering
python manage.py show-alerts --limit 20

# Automated test environment setup
python manage.py run-test
```

**All commands have:**
- ✅ Confirmation prompts for destructive operations
- ✅ Colorized output for easy reading
- ✅ Detailed feedback on what was done
- ✅ Error handling and validation

**Full documentation: See [COMMANDS_REFERENCE.md](COMMANDS_REFERENCE.md)**

---

## ⚙️ Standard Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual Environment (recommended)

### Installation Steps

1. **Clone/Setup Project**
   ```bash
   cd phishing
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   ```bash
   # Copy example env file
   cp .env.example .env
   
   # Edit .env and set your configuration (optional for development)
   ```

5. **Initialize Database**
   The database will be created automatically on first run with a default admin user:
   - **Username:** admin
   - **Password:** admin123
   - **⚠️ NOTE:** Change this password in production!

### Running the Application

```bash
python app.py
```

The application will start on: `http://localhost:5000`

Then open your browser and navigate to the above URL.

---

## Sprint 1 Features

### ✅ User Authentication
- Secure login system
- User registration
- Session management
- Role-based access (analyst, admin)

### ✅ Transaction Management
- Add new transactions
- View all transactions
- Filter suspicious transactions
- Transaction details view
- Real-time fraud detection

### ✅ Rule-Based Detection Engine
The system uses predefined rules to detect suspicious transactions:

1. **High Amount Threshold ($10,000)**
   - Flags transactions with amounts exceeding $10,000
   - Risk Score: +30

2. **Multiple Transactions in Short Time**
   - Detects if sender makes 5+ transactions within 60 minutes
   - Risk Score: +35

3. **Repeated Transaction Patterns**
   - Identifies when same sender-receiver pair occurs 3+ times
   - Risk Score: +25

4. **Suspicious Account Patterns**
   - Flags accounts starting with 'SUSP_' prefix
   - Risk Score: +40

**Risk Level Calculation:**
- CRITICAL: Score ≥ 70
- HIGH: Score ≥ 50
- MEDIUM: Score ≥ 30
- LOW: Score < 30

### ✅ Alert Generation
- Automatic alert creation for suspicious transactions
- Risk level assignment
- Triggered rules documentation
- Alert status tracking (OPEN, INVESTIGATING, RESOLVED, FALSE_POSITIVE)

### ✅ Dashboard
- System overview with key metrics
- Total transactions count
- Suspicious transactions count
- Open alerts count
- Risk distribution charts
- Recent alerts visualization
- Quick action buttons

### ✅ Database Integration
- SQLite database (production-ready)
- Complete transaction history
- Alert tracking
- User management
- Audit trail with timestamps

### ✅ Report & Analytics
- Transaction list with filtering
- Suspicious transaction highlighting
- Transaction details view
- Alert management interface
- Status updates and notes

---

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user info

### Transactions
- `POST /api/transactions` - Create transaction
- `GET /api/transactions` - List transactions
- `GET /api/transactions/<id>` - Get transaction details

### Alerts
- `GET /api/alerts` - List alerts
- `PUT /api/alerts/<id>` - Update alert status/notes

### Dashboard
- `GET /api/dashboard/stats` - Get dashboard statistics

---

## Web Pages

- **Login** - `/login` - User authentication
- **Dashboard** - `/dashboard` - System overview
- **Transactions** - `/transactions` - Transaction management
- **Alerts** - `/alerts` - Alert management and review

---

## Production Deployment

### Before Going Live:

1. **Change Default Credentials**
   ```python
   # Edit app.py init_db() function
   # Create a strong admin password
   ```

2. **Set Strong Secret Key**
   ```bash
   # Generate secure key
   python -c "import secrets; print(secrets.token_hex(32))"
   
   # Add to .env
   SECRET_KEY=your_generated_key_here
   ```

3. **Switch to Production Database**
   - Consider PostgreSQL or MySQL for production
   - Update DATABASE_URL in .env

4. **Enable HTTPS**
   - Deploy behind reverse proxy (nginx)
   - Configure SSL certificates

5. **Logging & Monitoring**
   - Enable comprehensive logging
   - Set up monitoring and alerts

6. **Performance Optimization**
   - Add database indexing
   - Implement caching
   - Add rate limiting

---

## Database Schema

### users table
- id (Primary Key)
- username (Unique, Indexed)
- password_hash
- email (Unique, Indexed)
- full_name
- role (analyst, admin)
- is_active
- created_at
- last_login

### transactions table
- id (Primary Key)
- transaction_id (Unique, Indexed)
- sender_account (Indexed)
- receiver_account
- amount
- currency
- transaction_date
- is_suspicious (Indexed)
- risk_level
- detection_reason
- created_at (Indexed)
- updated_at

### alerts table
- id (Primary Key)
- transaction_id (Foreign Key, Unique)
- risk_level
- status
- triggered_rules (JSON)
- analyst_notes
- created_at (Indexed)
- updated_at
- assigned_to (Foreign Key)

---

## 📖 Documentation Guide

This project includes comprehensive documentation for different user needs:

| Document | Purpose | Best For |
|----------|---------|----------|
| **[QUICKREF.md](QUICKREF.md)** | Commands & credentials on one page | Quick lookup |
| **[QUICK_START.md](QUICK_START.md)** | Fast setup paths and demo | New users, DevOps |
| **[SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md)** | Architecture & system design | Developers, Architects |
| **[TEST_ENVIRONMENT.md](TEST_ENVIRONMENT.md)** | Test environment setup & data generation | QA, Testing teams |
| **[COMMANDS_REFERENCE.md](COMMANDS_REFERENCE.md)** | Complete CLI command documentation | Developers, DevOps |
| **[TESTING_GUIDE.md](TESTING_GUIDE.md)** | Manual testing procedures | QA, Analysts |
| **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** | Project architecture & file organization | Developers |

**Choose your path:**
- 📋 I need quick commands → **[QUICKREF.md](QUICKREF.md)** (print-friendly!)
- 🏃 I want to run it NOW → **[QUICK_START.md](QUICK_START.md)**
- 🏗️ I want system details → **[SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md)**
- 🧪 I want to test with data → **[TEST_ENVIRONMENT.md](TEST_ENVIRONMENT.md)**
- ⚙️ I want CLI commands → **[COMMANDS_REFERENCE.md](COMMANDS_REFERENCE.md)**
- 📋 I want test procedures → **[TESTING_GUIDE.md](TESTING_GUIDE.md)**
- 📁 I want code structure → **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)**

---

## Troubleshooting

### Database Issues
```bash
# Reset database (development only)
rm aml_system.db
python app.py  # Will recreate with fresh data
```

### Port Already in Use
```bash
# Change port in app.py
app.run(debug=False, host='0.0.0.0', port=5001)
```

### Import Errors
```bash
# Reinstall requirements
pip install --force-reinstall -r requirements.txt
```

---

## 🚀 Getting Started Checklist

- [ ] Install Python 3.8+
- [ ] Clone/setup project in `phishing` directory
- [ ] Run `python run_test.py` to start with demo data
- [ ] Open `http://localhost:5000` in browser
- [ ] Login with `admin` / `admin123`
- [ ] Explore dashboard, transactions, and alerts
- [ ] Read [COMMANDS_REFERENCE.md](COMMANDS_REFERENCE.md) for advanced features
- [ ] Customize test data with `python manage.py seed-db --count 500`

---

## Support & Additional Resources

### Project Documentation
- 📖 [QUICK_START.md](QUICK_START.md) - Fast setup guide
- 🧪 [TEST_ENVIRONMENT.md](TEST_ENVIRONMENT.md) - Testing documentation
- ⚙️ [COMMANDS_REFERENCE.md](COMMANDS_REFERENCE.md) - CLI commands
- 📋 [TESTING_GUIDE.md](TESTING_GUIDE.md) - Testing procedures
- 🏗️ [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Architecture

### External Resources
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Click CLI Documentation](https://click.palletsprojects.com/)
- [Python Documentation](https://docs.python.org/)

---

## Version History

**Sprint 1 (Current)** ✅ COMPLETE
- ✅ User Authentication System
- ✅ Transaction Management & Entry
- ✅ Rule-Based Fraud Detection (4 rules)
- ✅ Alert Generation & Management
- ✅ Dashboard with Statistics
- ✅ Test Environment & Data Generation
- ✅ CLI Management Tools
- ✅ Responsive Web UI

**Future Sprints:**
- 🔄 AI/ML-based detection
- 🔄 Real-time monitoring
- 🔄 Advanced analytics & reporting
- 🔄 Email notifications
- 🔄 Multi-tenancy support
- Integration with external APIs
- Mobile application

---

## 📂 File Inventory

### Core Application Files
| File | Size | Purpose |
|------|------|---------|
| [app.py](app.py) | ~2000 lines | Flask backend with all business logic, API endpoints, database models |
| [manage.py](manage.py) | ~300 lines | CLI management tool (seed-db, clear-db, reset-db, show-stats, etc.) |
| [seed_data.py](seed_data.py) | ~400 lines | Dummy data generator with 5 test users and realistic transaction patterns |
| [run_test.py](run_test.py) | ~150 lines | Automated test environment setup (one-command startup) |

### Configuration & Scripts
| File | Purpose |
|------|---------|
| [requirements.txt](requirements.txt) | Python dependencies (Flask, SQLAlchemy, Click, etc.) |
| [setup.sh](setup.sh) | Linux/Mac automated setup script |
| [setup.bat](setup.bat) | Windows automated setup script |
| [run_test.sh](run_test.sh) | Linux/Mac interactive test menu |
| [run_test.bat](run_test.bat) | Windows interactive test menu |
| [.env.example](.env.example) | Environment variables template |
| [.gitignore](.gitignore) | Git ignore patterns |
| [Dockerfile](Dockerfile) | Docker image configuration |
| [docker-compose.yml](docker-compose.yml) | Docker Compose setup |

### Documentation Files
| File | Purpose |
|------|---------|
| [README.md](README.md) | Project overview and quick start (YOU ARE HERE) |
| [QUICK_START.md](QUICK_START.md) | Fast setup paths and demo credentials |
| [TEST_ENVIRONMENT.md](TEST_ENVIRONMENT.md) | Test environment setup and data generation guide |
| [COMMANDS_REFERENCE.md](COMMANDS_REFERENCE.md) | Complete CLI commands documentation |
| [TESTING_GUIDE.md](TESTING_GUIDE.md) | Manual testing procedures and scenarios |
| [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | Project architecture and file organization |

### Frontend Templates (HTML)
| Path | Purpose |
|------|---------|
| [templates/base.html](templates/base.html) | Base template with navigation and layout |
| [templates/login.html](templates/login.html) | User login page |
| [templates/dashboard.html](templates/dashboard.html) | Main dashboard with statistics |
| [templates/transactions.html](templates/transactions.html) | Transaction management interface |
| [templates/alerts.html](templates/alerts.html) | Alert management and review |
| [templates/404.html](templates/404.html) | 404 error page |
| [templates/500.html](templates/500.html) | 500 error page |

### Frontend Assets
| Path | Purpose |
|------|---------|
| [static/css/style.css](static/css/style.css) | Production styling (~650 lines, responsive design) |
| [static/js/main.js](static/js/main.js) | JavaScript utilities (API calls, formatting) |

### Data Directories
| Path | Purpose |
|------|---------|
| `instance/` | SQLite database and instance files (auto-created) |
| `venv/` | Python virtual environment (auto-created by setup scripts) |

### Development Directories
| Path | Purpose |
|------|---------|
| [.vscode/](.vscode/) | VS Code configuration files |

---

## 💡 Next Steps

1. **Quick Start**: Run `python run_test.py` to see the system in action
2. **Explore**: Open `http://localhost:5000` and login with demo credentials
3. **Test Features**: Try adding transactions, reviewing alerts, filtering suspicious items
4. **Customize**: Read [COMMANDS_REFERENCE.md](COMMANDS_REFERENCE.md) to customize test data
5. **integrate**: Refer to [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) to understand the codebase for customization
6. **Deploy**: Use [Dockerfile](Dockerfile) and [docker-compose.yml](docker-compose.yml) for containerized deployment

---

**Happy Testing! 🎉 The system is ready to use. Start with `python run_test.py` now!**
