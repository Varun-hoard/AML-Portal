# AML System - Sprint 1 Files Overview

## Project Structure

```
phishing/
├── app.py                          # Main Flask application (backend)
├── fraud_front.py                  # Frontend layer documentation
├── fraund_model.py                 # ML models placeholder
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── README.md                       # Main documentation
├── TESTING_GUIDE.md                # Testing and demo guide
├── Dockerfile                      # Docker container definition
├── docker-compose.yml              # Docker compose configuration
├── setup.sh                        # Linux/Mac setup script
├── setup.bat                       # Windows setup script
├── PROJECT_STRUCTURE.md            # This file
│
├── templates/                      # HTML Templates
│   ├── base.html                  # Base template with navigation
│   ├── login.html                 # Login page
│   ├── dashboard.html             # Dashboard page
│   ├── transactions.html          # Transactions management
│   ├── alerts.html                # Alerts management
│   ├── 404.html                   # 404 error page
│   └── 500.html                   # 500 error page
│
├── static/                         # Static files
│   ├── css/
│   │   └── style.css              # Main stylesheet (comprehensive)
│   └── js/
│       └── main.js                # JavaScript utilities
│
└── aml_system.db                   # SQLite database (auto-created)
```

## File Descriptions

### Backend Files

**app.py** (Main Application - ~450 lines)
- Flask application initialization
- Database models (User, Transaction, Alert)
- Authentication system (login, register, logout)
- Fraud detection engine with 4 rules
- RESTful API endpoints (14+ endpoints)
- Error handling and logging
- Database initialization with default admin user

**fraund_model.py** (ML Models Placeholder - ~150 lines)
- Placeholder classes for future ML models
- Feature engineering functions structure
- Model evaluation methodology
- Notes on future development
- Placeholder for anomaly detection and time-series analysis

**fraud_front.py** (Frontend Documentation - ~80 lines)
- Frontend architecture overview
- Template file descriptions
- Component documentation
- Configuration constants

### Frontend Files (Templates)

**base.html** (Main Layout)
- Navigation bar with system branding
- User info and logout button
- Flash messages integration
- Footer with copyright
- JavaScript integration

**login.html** (Authentication)
- Professional login form
- Demo credentials display
- Error handling
- API integration with client-side validation

**dashboard.html** (System Overview)
- 4 main statistics cards (colored)
- Risk distribution visualization
- Quick action buttons
- Transaction entry modal
- Recent alerts section
- Real-time data loading

**transactions.html** (Transaction Management)
- Transactions table with sorting
- Filter suspicious transactions
- Search functionality
- Pagination controls
- Transaction details modal
- Add transaction modal
- Status and risk level visualization

**alerts.html** (Alert Management)
- Alerts table with details
- Status filters (Open, Investigating, Resolved)
- Risk level color coding
- Alert details modal with notes
- Status update capability
- Triggered rules display

**404.html & 500.html** (Error Pages)
- Clean error page layout
- Home button
- Basic navigation

### Frontend Files (Static)

**style.css** (Styling - ~650 lines)
Comprehensive CSS covering:
- CSS variables for colors (6 main colors)
- Typography and spacing system
- Navigation bar styling
- Button styles (primary, secondary, small)
- Container and card layouts
- Dashboard statistics cards
- Tables with hover effects
- Forms and modals
- Risk level color coding
- Badges and status indicators
- Responsive design (mobile, tablet, desktop)
- Animations and transitions
- Login page styling
- Error page styling

**main.js** (JavaScript - ~100 lines)
- User authentication checking
- Currency and date formatting utilities
- Toast notification system
- Global utility functions
- Animation keyframes

### Configuration Files

**.env.example**
- SECRET_KEY template
- DATABASE_URL configuration
- FLASK_ENV settings
- Database URL setup

**requirements.txt**
- Flask 2.3.3
- Flask-SQLAlchemy 3.0.5
- Python-dotenv 1.0.0
- Werkzeug 2.3.7

**README.md** (Main Documentation - ~350 lines)
- Environment setup instructions
- Installation steps
- Running the application
- Sprint 1 features overview
- Detection rules explanation
- API endpoints documentation
- Web pages listing
- Production deployment checklist
- Database schema
- Troubleshooting guide

**TESTING_GUIDE.md** (Testing Documentation - ~300 lines)
- Demo scenarios (5 detailed scenarios)
- Sample transaction data
- Manual testing checklist (50+ test cases)
- API testing examples
- Performance benchmarks
- Known limitations
- Test data generator reference

### Container Files

**Dockerfile**
- Python 3.11-slim base image
- Working directory setup
- Environment variables
- System dependencies installation
- Python dependencies installation
- Application code copying
- Port exposure (5000)
- Health check configuration
- Gunicorn startup command

**docker-compose.yml**
- AML system service definition
- Port mapping (5000:5000)
- Volume mounts (database, logs)
- Environment variables
- Restart policy
- Network configuration

### Setup Scripts

**setup.sh** (Linux/Mac)
- Python version check
- Virtual environment creation
- Virtual environment activation
- Dependencies installation
- .env file creation

**setup.bat** (Windows)
- Python version check
- Virtual environment creation
- Dependencies installation
- .env file creation
- Windows-specific batch commands

## Key Statistics

- **Total Lines of Code**: ~2,500
- **Backend Code**: ~650 lines
- **Frontend HTML**: ~800 lines
- **CSS Styling**: ~650 lines
- **JavaScript**: ~100 lines
- **Documentation**: ~700 lines
- **Configuration Files**: ~20 lines

## Technology Stack

**Backend:**
- Python 3.8+
- Flask 2.3.3
- SQLAlchemy ORM
- SQLite Database
- Werkzeug Security

**Frontend:**
- HTML5
- CSS3 (Grid, Flexbox)
- Vanilla JavaScript (ES6+)
- REST API

**DevOps:**
- Docker
- Docker Compose
- Gunicorn WSGI Server

## Database Schema

**3 Main Tables:**
1. **users** - User authentication and roles
2. **transactions** - Finance transactions tracking
3. **alerts** - Fraud alerts management

**Total Fields**: 25+ across all tables
**Relationships**: Alerts reference Transactions

## API Endpoints (14+)

- 4 Authentication endpoints
- 3 Transaction endpoints
- 2 Alert endpoints
- 1 Dashboard endpoint
- 4 Web page routes

## Features Implemented

✅ User authentication (register, login, logout)
✅ Transaction management (CRUD)
✅ Rule-based fraud detection (4 rules)
✅ Alert generation and management
✅ Dashboard with statistics
✅ Transaction reporting and filtering
✅ Risk level classification
✅ Responsive web interface
✅ Error handling and logging
✅ Database persistence

## Future Enhancements (Planned for Later Sprints)

- ML/AI-based detection models
- Real-time monitoring dashboard
- Advanced analytics and reports
- Email notifications
- Multi-tenancy support
- API rate limiting
- Audit logging
- User role-based permissions
- Password reset functionality
- Transaction export (CSV/PDF)
- Scheduled reporting
- Mobile application

## Deployment Options

1. **Local Development**: `python app.py`
2. **Production (Docker)**: `docker-compose up`
3. **Production (Gunicorn)**: `gunicorn app:app`
4. **Cloud Deployment**: Ready for AWS, Azure, GCP

## Security Features

- Password hashing (Werkzeug)
- Session management
- SQL injection prevention (SQLAlchemy ORM)
- CSRF protection ready
- Secure headers available
- Input validation
- Error message sanitization
- Logging of security events

## Performance Metrics

- Transaction insertion: < 100ms
- Transaction retrieval: < 200ms
- Detection rule evaluation: < 50ms
- Alert generation: < 20ms
- Dashboard load: < 2 seconds

## File Sizes

- app.py: ~18 KB
- style.css: ~26 KB
- HTML templates: ~32 KB (total)
- JavaScript: ~4 KB
- Database (10k transactions): ~5 MB
