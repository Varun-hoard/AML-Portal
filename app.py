"""
Anti-Money Laundering (AML) System - Sprint 1
Main Flask Application
"""

import os
import json
import csv
import io
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///aml_system.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ======================== Database Models ========================

class User(db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    full_name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='analyst')  # analyst, admin
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'role': self.role
        }


class Transaction(db.Model):
    """Transaction model for AML tracking"""
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    sender_account = db.Column(db.String(50), nullable=False, index=True)
    receiver_account = db.Column(db.String(50), nullable=False, index=True)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    transaction_date = db.Column(db.DateTime, nullable=False)
    is_suspicious = db.Column(db.Boolean, default=False, index=True)
    risk_level = db.Column(db.String(20), default='LOW')  # LOW, MEDIUM, HIGH, CRITICAL
    detection_reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    alert = db.relationship('Alert', backref='transaction', uselist=False, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'transaction_id': self.transaction_id,
            'sender_account': self.sender_account,
            'receiver_account': self.receiver_account,
            'amount': self.amount,
            'currency': self.currency,
            'transaction_date': self.transaction_date.isoformat(),
            'is_suspicious': self.is_suspicious,
            'risk_level': self.risk_level,
            'detection_reason': self.detection_reason,
            'created_at': self.created_at.isoformat()
        }


class Alert(db.Model):
    """Alert model for suspicious transactions"""
    __tablename__ = 'alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), nullable=False, unique=True)
    risk_level = db.Column(db.String(20), nullable=False)  # LOW, MEDIUM, HIGH, CRITICAL
    status = db.Column(db.String(20), default='OPEN')  # OPEN, INVESTIGATING, RESOLVED, FALSE_POSITIVE
    triggered_rules = db.Column(db.Text)  # JSON array of rule names
    analyst_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def to_dict(self):
        return {
            'id': self.id,
            'transaction_id': self.transaction_id,
            'risk_level': self.risk_level,
            'status': self.status,
            'triggered_rules': json.loads(self.triggered_rules) if self.triggered_rules else [],
            'analyst_notes': self.analyst_notes,
            'created_at': self.created_at.isoformat()
        }


# ======================== Authentication ========================

def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.path.startswith('/api/'):
                return jsonify({'error': 'Unauthorized'}), 401
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validation
        if not data or not data.get('username') or not data.get('password') or not data.get('email'):
            return jsonify({'error': 'Missing required fields'}), 400
            
        if len(data.get('password', '')) < 6:
            return jsonify({'error': 'Password must be at least 6 characters long'}), 400
        
        # Check if user exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 409
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 409
        
        # Create user
        user = User(
            username=data['username'],
            email=data['email'],
            full_name=data.get('full_name', data['username']),
            role='analyst'
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        logger.info(f"New user registered: {user.username}")
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict()
        }), 201
    
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/auth/login', methods=['POST'])
def api_login():
    """API login endpoint"""
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Missing credentials'}), 400
        
        user = User.query.filter_by(username=data['username']).first()
        
        if not user or not user.check_password(data['password']):
            logger.warning(f"Failed login attempt for username: {data['username']}")
            return jsonify({'error': 'Invalid credentials'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'User account is inactive'}), 403
        
        session['user_id'] = user.id
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        logger.info(f"User logged in: {user.username}")
        
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict()
        }), 200
    
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/auth/logout', methods=['POST'])
@login_required
def api_logout():
    """Logout endpoint"""
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200


@app.route('/api/auth/me', methods=['GET'])
@login_required
def get_current_user():
    """Get current user info"""
    user = User.query.get(session['user_id'])
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({'error': 'User not found'}), 404


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health heartbeat endpoint"""
    try:
        # Check DB connection
        db.session.execute(db.text('SELECT 1'))
        return jsonify({'status': 'healthy', 'database': 'connected', 'timestamp': datetime.utcnow().isoformat()}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e), 'timestamp': datetime.utcnow().isoformat()}), 503


# ======================== Detection Rules ========================

class FraudDetectionEngine:
    """Rule-based fraud detection engine"""
    
    AMOUNT_THRESHOLD = 10000  # High amount transaction
    MULTIPLE_TRANSACTION_THRESHOLD = 5  # Multiple transactions in short time
    TIME_WINDOW_MINUTES = 60  # Time window for multiple transaction detection
    
    @staticmethod
    def detect_suspicious_transaction(sender, receiver, amount, transaction_date):
        """
        Detect suspicious transactions based on rules
        Returns: (is_suspicious, risk_level, reasons)
        """
        reasons = []
        risk_score = 0
        
        # Rule 1: Check for high amount transactions
        if amount > FraudDetectionEngine.AMOUNT_THRESHOLD:
            reasons.append("High transaction amount")
            risk_score += 30
        
        # Rule 2: Check for multiple transactions from same sender in short time
        time_threshold = transaction_date - timedelta(minutes=FraudDetectionEngine.TIME_WINDOW_MINUTES)
        recent_transactions = Transaction.query.filter(
            Transaction.sender_account == sender,
            Transaction.transaction_date >= time_threshold,
            Transaction.transaction_date <= transaction_date
        ).count()
        
        if recent_transactions >= FraudDetectionEngine.MULTIPLE_TRANSACTION_THRESHOLD:
            reasons.append(f"Multiple transactions ({recent_transactions}) in short time")
            risk_score += 35
        
        # Rule 3: Check for rapid round-robin transactions (same sender and receiver patterns)
        sender_receiver_pair = Transaction.query.filter(
            Transaction.sender_account == sender,
            Transaction.receiver_account == receiver,
            Transaction.transaction_date >= time_threshold,
            Transaction.transaction_date <= transaction_date
        ).count()
        
        if sender_receiver_pair >= 3:
            reasons.append("Repeated transaction pattern detected")
            risk_score += 25
        
        # Rule 4: Check for suspicious account patterns (known patterns)
        if sender.startswith('SUSP_') or receiver.startswith('SUSP_'):
            reasons.append("Suspicious account pattern detected")
            risk_score += 40
        
        # Determine risk level based on score
        if risk_score >= 70:
            risk_level = 'CRITICAL'
        elif risk_score >= 50:
            risk_level = 'HIGH'
        elif risk_score >= 30:
            risk_level = 'MEDIUM'
        else:
            risk_level = 'LOW'
        
        is_suspicious = risk_score >= 30
        
        return is_suspicious, risk_level, reasons


# ======================== Transaction Endpoints ========================

@app.route('/api/transactions', methods=['POST'])
@login_required
def create_transaction():
    """Create a new transaction and run detection"""
    try:
        data = request.get_json()
        
        # Validation
        required_fields = ['sender_account', 'receiver_account', 'amount', 'transaction_date']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        try:
            amount = float(data['amount'])
            if amount <= 0:
                return jsonify({'error': 'Amount must be positive'}), 400
        except ValueError:
            return jsonify({'error': 'Invalid amount'}), 400
        
        try:
            transaction_date = datetime.fromisoformat(data['transaction_date'].replace('Z', '+00:00'))
        except ValueError as e:
            return jsonify({'error': f'Invalid transaction date format: {str(e)}'}), 400
        
        # Check for duplicate transaction
        transaction_id = f"TXN-{int(datetime.utcnow().timestamp())}-{data['sender_account'][-4:]}"
        
        # Run fraud detection
        is_suspicious, risk_level, reasons = FraudDetectionEngine.detect_suspicious_transaction(
            data['sender_account'],
            data['receiver_account'],
            amount,
            transaction_date
        )
        
        # Create transaction
        transaction = Transaction(
            transaction_id=transaction_id,
            sender_account=data['sender_account'],
            receiver_account=data['receiver_account'],
            amount=amount,
            currency=data.get('currency', 'USD'),
            transaction_date=transaction_date,
            is_suspicious=is_suspicious,
            risk_level=risk_level,
            detection_reason=' | '.join(reasons) if reasons else None
        )
        
        db.session.add(transaction)
        db.session.flush()
        
        # Create alert if suspicious
        if is_suspicious:
            alert = Alert(
                transaction_id=transaction.id,
                risk_level=risk_level,
                status='OPEN',
                triggered_rules=json.dumps([r.split('(')[0].strip() for r in reasons])
            )
            db.session.add(alert)
        
        db.session.commit()
        
        logger.info(f"Transaction created: {transaction_id}, Suspicious: {is_suspicious}")
        
        return jsonify({
            'message': 'Transaction created successfully',
            'transaction': transaction.to_dict(),
            'alert': alert.to_dict() if is_suspicious else None
        }), 201
    
    except Exception as e:
        logger.error(f"Error creating transaction: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/transactions', methods=['GET'])
@login_required
def get_transactions():
    """Get all transactions with filtering"""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        suspicious_only = request.args.get('suspicious', 'false').lower() == 'true'
        
        query = Transaction.query
        
        if suspicious_only:
            query = query.filter_by(is_suspicious=True)
        
        # Apply sorting
        query = query.order_by(Transaction.created_at.desc())
        
        # Paginate
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'transactions': [t.to_dict() for t in paginated.items],
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': page
        }), 200
    
    except Exception as e:
        logger.error(f"Error fetching transactions: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/transactions/<int:transaction_id>', methods=['GET'])
@login_required
def get_transaction(transaction_id):
    """Get a specific transaction"""
    try:
        transaction = Transaction.query.get(transaction_id)
        if not transaction:
            return jsonify({'error': 'Transaction not found'}), 404
        
        result = transaction.to_dict()
        if transaction.alert:
            result['alert'] = transaction.alert.to_dict()
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Error fetching transaction: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


# ======================== Dashboard Endpoints ========================

@app.route('/api/dashboard/stats', methods=['GET'])
@login_required
def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        total_transactions = Transaction.query.count()
        suspicious_transactions = Transaction.query.filter_by(is_suspicious=True).count()
        open_alerts = Alert.query.filter_by(status='OPEN').count()
        
        # Risk distribution
        risk_distribution = db.session.query(
            Transaction.risk_level,
            db.func.count(Transaction.id).label('count')
        ).group_by(Transaction.risk_level).all()
        
        risk_dist = {risk: count for risk, count in risk_distribution}
        
        # Total transaction amount
        total_amount = db.session.query(
            db.func.sum(Transaction.amount)
        ).filter_by(is_suspicious=False).scalar() or 0
        
        suspicious_amount = db.session.query(
            db.func.sum(Transaction.amount)
        ).filter_by(is_suspicious=True).scalar() or 0
        
        return jsonify({
            'total_transactions': total_transactions,
            'suspicious_transactions': suspicious_transactions,
            'suspicious_percentage': round((suspicious_transactions / total_transactions * 100), 2) if total_transactions > 0 else 0,
            'open_alerts': open_alerts,
            'total_amount': round(total_amount, 2),
            'suspicious_amount': round(suspicious_amount, 2),
            'risk_distribution': {
                'LOW': risk_dist.get('LOW', 0),
                'MEDIUM': risk_dist.get('MEDIUM', 0),
                'HIGH': risk_dist.get('HIGH', 0),
                'CRITICAL': risk_dist.get('CRITICAL', 0)
            }
        }), 200
    
    except Exception as e:
        logger.error(f"Error fetching dashboard stats: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


# ======================== Alert Endpoints ========================

@app.route('/api/alerts', methods=['GET'])
@login_required
def get_alerts():
    """Get all alerts"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        paginated = Alert.query.order_by(Alert.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'alerts': [a.to_dict() for a in paginated.items],
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': page
        }), 200
    
    except Exception as e:
        logger.error(f"Error fetching alerts: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/alerts/<int:alert_id>', methods=['GET', 'PUT'])
@login_required
def get_or_update_alert(alert_id):
    """Get alert details or update alert status and notes"""
    try:
        alert = Alert.query.get(alert_id)
        if not alert:
            return jsonify({'error': 'Alert not found'}), 404
        
        # GET request - return alert details
        if request.method == 'GET':
            return jsonify(alert.to_dict()), 200
        
        # PUT request - update alert
        data = request.get_json()
        
        if 'status' in data:
            alert.status = data['status']
        
        if 'analyst_notes' in data:
            alert.analyst_notes = data['analyst_notes']
        
        alert.updated_at = datetime.utcnow()
        db.session.commit()
        
        logger.info(f"Alert {alert_id} updated: {data}")
        
        return jsonify({
            'message': 'Alert updated successfully',
            'alert': alert.to_dict()
        }), 200
    
    except Exception as e:
        logger.error(f"Error with alert {alert_id}: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500


# ======================== Web Routes ========================

@app.route('/')
def index():
    """Redirect to dashboard or login"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        return redirect(url_for('dashboard'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard page"""
    return render_template('dashboard.html')


@app.route('/transactions')
@login_required
def transactions():
    """Transactions page"""
    return render_template('transactions.html')


@app.route('/alerts')
@login_required
def alerts():
    """Alerts page"""
    return render_template('alerts.html')


# ======================== NEW FUNCTIONALITIES ========================

# 1. CSV EXPORT FUNCTIONALITY
@app.route('/api/export/transactions', methods=['GET'])
@login_required
def export_transactions_csv():
    """Export transactions to CSV"""
    try:
        # Query all transactions
        transactions = Transaction.query.all()
        
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write headers
        writer.writerow([
            'Transaction ID',
            'Sender Account',
            'Receiver Account',
            'Amount',
            'Currency',
            'Date',
            'Risk Level',
            'Is Suspicious',
            'Detection Reason',
            'Created At'
        ])
        
        # Write data rows
        for txn in transactions:
            writer.writerow([
                txn.transaction_id,
                txn.sender_account,
                txn.receiver_account,
                txn.amount,
                txn.currency,
                txn.transaction_date.isoformat() if txn.transaction_date else '',
                txn.risk_level,
                'Yes' if txn.is_suspicious else 'No',
                txn.detection_reason or '',
                txn.created_at.isoformat()
            ])
        
        # Prepare response
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode()),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'transactions_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}.csv'
        )
    
    except Exception as e:
        logger.error(f"Error exporting transactions: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/export/alerts', methods=['GET'])
@login_required
def export_alerts_csv():
    """Export alerts to CSV"""
    try:
        # Query all alerts with transaction data
        alerts = Alert.query.all()
        
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write headers
        writer.writerow([
            'Alert ID',
            'Transaction ID',
            'Risk Level',
            'Status',
            'Triggered Rules',
            'Analyst Notes',
            'Created At',
            'Updated At',
            'Assigned To'
        ])
        
        # Write data rows
        for alert in alerts:
            writer.writerow([
                alert.id,
                alert.transaction_id,
                alert.risk_level,
                alert.status,
                ','.join(json.loads(alert.triggered_rules)) if alert.triggered_rules else '',
                alert.analyst_notes or '',
                alert.created_at.isoformat(),
                alert.updated_at.isoformat(),
                alert.assigned_to or ''
            ])
        
        # Prepare response
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode()),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'alerts_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}.csv'
        )
    
    except Exception as e:
        logger.error(f"Error exporting alerts: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


# 2. ADVANCED STATISTICS ENDPOINT
@app.route('/api/dashboard/advanced-stats', methods=['GET'])
@login_required
def get_advanced_stats():
    """Get advanced analytics and statistics"""
    try:
        # Alert status distribution
        alert_status = db.session.query(
            Alert.status,
            db.func.count(Alert.id).label('count')
        ).group_by(Alert.status).all()
        
        status_dist = {status: count for status, count in alert_status}
        
        # Alerts by risk level
        alert_risk = db.session.query(
            Alert.risk_level,
            db.func.count(Alert.id).label('count')
        ).group_by(Alert.risk_level).all()
        
        risk_dist = {risk: count for risk, count in alert_risk}
        
        # Average transaction amount by risk level
        avg_amounts = db.session.query(
            Transaction.risk_level,
            db.func.avg(Transaction.amount).label('avg_amount'),
            db.func.count(Transaction.id).label('count')
        ).group_by(Transaction.risk_level).all()
        
        avg_by_risk = {
            risk: {'average': round(avg, 2), 'count': count}
            for risk, avg, count in avg_amounts
        }
        
        # Transactions in last 7 days
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        recent_suspicious = Transaction.query.filter(
            Transaction.created_at >= seven_days_ago,
            Transaction.is_suspicious == True
        ).count()
        
        recent_total = Transaction.query.filter(
            Transaction.created_at >= seven_days_ago
        ).count()
        
        # Most common detection reasons
        detection_reasons = db.session.query(
            Transaction.detection_reason,
            db.func.count(Transaction.id).label('count')
        ).filter(Transaction.detection_reason != None).group_by(
            Transaction.detection_reason
        ).order_by(db.func.count(Transaction.id).desc()).limit(5).all()
        
        reasons = [{'reason': reason, 'count': count} for reason, count in detection_reasons]
        
        return jsonify({
            'alert_status_distribution': {
                'OPEN': status_dist.get('OPEN', 0),
                'INVESTIGATING': status_dist.get('INVESTIGATING', 0),
                'RESOLVED': status_dist.get('RESOLVED', 0),
                'FALSE_POSITIVE': status_dist.get('FALSE_POSITIVE', 0)
            },
            'alerts_by_risk_level': {
                'LOW': risk_dist.get('LOW', 0),
                'MEDIUM': risk_dist.get('MEDIUM', 0),
                'HIGH': risk_dist.get('HIGH', 0),
                'CRITICAL': risk_dist.get('CRITICAL', 0)
            },
            'average_transaction_by_risk': avg_by_risk,
            'recent_7_days': {
                'total_transactions': recent_total,
                'suspicious_transactions': recent_suspicious,
                'suspicious_percentage': round((recent_suspicious / recent_total * 100), 2) if recent_total > 0 else 0
            },
            'top_detection_reasons': reasons
        }), 200
    
    except Exception as e:
        logger.error(f"Error fetching advanced stats: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


# 3. BULK ALERT ACTIONS
@app.route('/api/alerts/bulk-update', methods=['POST'])
@login_required
def bulk_update_alerts():
    """Update multiple alerts at once"""
    try:
        data = request.get_json()
        
        if not data or 'alert_ids' not in data or not data.get('update_data'):
            return jsonify({'error': 'Missing required fields (alert_ids, update_data)'}), 400
        
        alert_ids = data['alert_ids']
        update_data = data['update_data']
        
        if not isinstance(alert_ids, list) or len(alert_ids) == 0:
            return jsonify({'error': 'alert_ids must be a non-empty array'}), 400
        
        # Update alerts
        updated_count = 0
        for alert_id in alert_ids:
            alert = Alert.query.get(alert_id)
            if alert:
                if 'status' in update_data:
                    alert.status = update_data['status']
                if 'analyst_notes' in update_data:
                    alert.analyst_notes = update_data['analyst_notes']
                if 'assigned_to' in update_data:
                    alert.assigned_to = update_data['assigned_to']
                
                alert.updated_at = datetime.utcnow()
                db.session.add(alert)
                updated_count += 1
        
        db.session.commit()
        logger.info(f"Bulk updated {updated_count} alerts: {update_data}")
        
        return jsonify({
            'message': f'Successfully updated {updated_count} alerts',
            'updated_count': updated_count
        }), 200
    
    except Exception as e:
        logger.error(f"Error in bulk update: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500


# ======================== Error Handlers ========================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Not found'}), 404
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Internal server error'}), 500
    return render_template('500.html'), 500


# ======================== Create Tables ========================

def init_db():
    """Initialize database"""
    with app.app_context():
        db.create_all()
        
        # Create default admin user if not exists
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@aml-system.local',
                full_name='System Administrator',
                role='admin'
            )
            admin.set_password('admin123')  # Change in production!
            db.session.add(admin)
            db.session.commit()
            logger.info("Default admin user created")


if __name__ == '__main__':
    init_db()
    app.run(debug=False, host='0.0.0.0', port=5000)
