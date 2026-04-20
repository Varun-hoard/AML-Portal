"""
AML System - Database Management & CLI

Provides commands to:
- Seed database with dummy data
- Clear all data
- Reset database
- Run in test mode with sample data
"""

import os
import sys
import click
from datetime import datetime, timedelta
import random
import json

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User, Transaction, Alert
from seed_data import generate_dummy_data, DUMMY_USERS

@click.group()
def cli():
    """AML System Management Commands"""
    pass


@cli.command()
@click.option('--count', default=100, help='Number of transactions to generate')
@click.option('--users', default=5, help='Number of user accounts to create')
def seed_db(count, users):
    """Populate database with dummy data for testing"""
    click.echo(click.style('🌱 Seeding database...', fg='green', bold=True))
    
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            click.echo(click.style('✅ Tables created', fg='green'))
            
            # Create users
            click.echo(f'👥 Creating {users} test users...')
            test_users = []
            for i in range(users):
                user_data = DUMMY_USERS[i % len(DUMMY_USERS)]
                user = User(
                    username=user_data['username'],
                    email=user_data['email'],
                    full_name=user_data['full_name'],
                    role=user_data['role']
                )
                user.set_password(user_data['password'])
                db.session.add(user)
                test_users.append(user)
            
            # Also create default admin if not exists
            if not User.query.filter_by(username='admin').first():
                admin = User(
                    username='admin',
                    email='admin@aml-system.local',
                    full_name='System Administrator',
                    role='admin'
                )
                admin.set_password('admin123')
                db.session.add(admin)
                test_users.append(admin)
            
            db.session.commit()
            click.echo(click.style(f'✅ Created {len(test_users)} users', fg='green'))
            
            # Generate and add transactions
            click.echo(f'💰 Creating {count} dummy transactions...')
            transactions_data = generate_dummy_data(count)
            
            for txn_data in transactions_data:
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
                    alert = Alert(
                        transaction_id=transaction.id,
                        risk_level=txn_data['risk_level'],
                        status=random.choice(['OPEN', 'INVESTIGATING', 'OPEN']),
                        triggered_rules=txn_data.get('triggered_rules', '[]'),
                        analyst_notes=txn_data.get('analyst_notes', None)
                    )
                    db.session.add(alert)
            
            db.session.commit()
            click.echo(click.style(f'✅ Created {count} transactions', fg='green'))
            
            # Print credentials
            click.echo('\n' + click.style('=' * 50, fg='cyan'))
            click.echo(click.style('📋 Test Credentials:', fg='cyan', bold=True))
            click.echo(click.style('=' * 50, fg='cyan'))
            click.echo(f'Default Admin:')
            click.echo(f'  Username: {click.style("admin", fg="yellow")}')
            click.echo(f'  Password: {click.style("admin123", fg="yellow")}')
            click.echo(f'\nOther Test Users:')
            for user in DUMMY_USERS[:users]:
                click.echo(f'  {user["username"]:<15} / {user["password"]}')
            click.echo(click.style('=' * 50, fg='cyan'))
            
            # Print statistics
            transaction_count = Transaction.query.count()
            suspicious_count = Transaction.query.filter_by(is_suspicious=True).count()
            alert_count = Alert.query.count()
            
            click.echo('\n' + click.style('📊 Database Statistics:', fg='cyan', bold=True))
            click.echo(f'  Total Transactions: {transaction_count}')
            click.echo(f'  Suspicious Transactions: {suspicious_count}')
            click.echo(f'  Total Alerts: {alert_count}')
            
        except Exception as e:
            click.echo(click.style(f'❌ Error: {str(e)}', fg='red', bold=True))
            db.session.rollback()
            sys.exit(1)


@cli.command()
@click.confirmation_option(prompt='⚠️  This will delete ALL data. Are you sure?')
def clear_db():
    """Delete all data from database"""
    click.echo(click.style('🗑️  Clearing database...', fg='red', bold=True))
    
    with app.app_context():
        try:
            # Delete all data
            db.drop_all()
            click.echo(click.style('✅ All data deleted', fg='green'))
        except Exception as e:
            click.echo(click.style(f'❌ Error: {str(e)}', fg='red', bold=True))
            sys.exit(1)


@cli.command()
@click.confirmation_option(prompt='⚠️  This will reset the database. Are you sure?')
def reset_db():
    """Reset database (clear and recreate schema)"""
    click.echo(click.style('🔄 Resetting database...', fg='yellow', bold=True))
    
    with app.app_context():
        try:
            # Drop all tables
            db.drop_all()
            click.echo(click.style('✅ Dropped all tables', fg='green'))
            
            # Create fresh schema
            db.create_all()
            click.echo(click.style('✅ Created fresh schema', fg='green'))
            
            # Create default admin
            admin = User(
                username='admin',
                email='admin@aml-system.local',
                full_name='System Administrator',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            
            click.echo(click.style('✅ Database reset successfully', fg='green'))
            click.echo(f'Default admin created: admin / admin123')
            
        except Exception as e:
            click.echo(click.style(f'❌ Error: {str(e)}', fg='red', bold=True))
            db.session.rollback()
            sys.exit(1)


@cli.command()
@click.option('--count', default=100, help='Number of test transactions')
@click.option('--mode', type=click.Choice(['test', 'prod']), default='test', 
              help='Run mode (test or production)')
def run_test(count, mode):
    """Seed database and run Flask app in test mode"""
    if mode == 'test':
        click.echo(click.style('🧪 Starting in TEST mode...', fg='blue', bold=True))
        
        # Seed the database
        with app.app_context():
            db.create_all()
            
            # Check if data already exists
            if Transaction.query.count() == 0:
                click.echo('Seeding test data...')
                transactions_data = generate_dummy_data(count)
                
                for txn_data in transactions_data:
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
                    
                    if txn_data['is_suspicious']:
                        alert = Alert(
                            transaction_id=transaction.id,
                            risk_level=txn_data['risk_level'],
                            status=random.choice(['OPEN', 'INVESTIGATING']),
                            triggered_rules=txn_data.get('triggered_rules', '[]')
                        )
                        db.session.add(alert)
                
                db.session.commit()
            
            if not User.query.filter_by(username='admin').first():
                admin = User(
                    username='admin',
                    email='admin@aml-system.local',
                    full_name='System Administrator',
                    role='admin'
                )
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
        
        click.echo(click.style('✅ Test data ready', fg='green'))
        click.echo(click.style('🚀 Starting Flask app...', fg='green'))
        click.echo(click.style('📍 Open http://localhost:5000', fg='cyan'))
        click.echo(click.style('🔐 Login: admin / admin123', fg='cyan'))
        
        app.run(debug=True, host='0.0.0.0', port=5000)
    
    else:
        click.echo(click.style('🚀 Starting in PRODUCTION mode...', fg='green', bold=True))
        app.run(debug=False, host='0.0.0.0', port=5000)


@cli.command()
def show_stats():
    """Display database statistics"""
    with app.app_context():
        users = User.query.count()
        transactions = Transaction.query.count()
        suspicious = Transaction.query.filter_by(is_suspicious=True).count()
        alerts = Alert.query.count()
        
        click.echo(click.style('\n📊 Database Statistics:', fg='cyan', bold=True))
        click.echo(click.style('─' * 40, fg='cyan'))
        click.echo(f'Users:                    {click.style(str(users), fg="yellow")}')
        click.echo(f'Total Transactions:       {click.style(str(transactions), fg="yellow")}')
        click.echo(f'Suspicious Transactions:  {click.style(str(suspicious), fg="yellow")}')
        click.echo(f'Alerts Generated:         {click.style(str(alerts), fg="yellow")}')
        
        if transactions > 0:
            suspicious_pct = (suspicious / transactions) * 100
            click.echo(f'Suspicious Rate:          {click.style(f"{suspicious_pct:.1f}%", fg="red")}')
        
        click.echo(click.style('─' * 40, fg='cyan'))
        
        # Risk distribution
        risk_dist = db.session.query(
            Transaction.risk_level,
            db.func.count(Transaction.id).label('count')
        ).group_by(Transaction.risk_level).all()
        
        if risk_dist:
            click.echo(click.style('\n📈 Risk Distribution:', fg='cyan', bold=True))
            for risk, count in risk_dist:
                pct = (count / transactions * 100) if transactions > 0 else 0
                click.echo(f'  {risk:<10} {click.style(str(count), fg="yellow")} ({pct:.1f}%)')


@cli.command()
def show_users():
    """Display all users in database"""
    with app.app_context():
        users = User.query.all()
        
        if not users:
            click.echo(click.style('No users found', fg='yellow'))
            return
        
        click.echo(click.style('\n👥 Users in Database:', fg='cyan', bold=True))
        click.echo(click.style('─' * 70, fg='cyan'))
        click.echo(f'{"Username":<20} {"Email":<30} {"Role":<10}')
        click.echo(click.style('─' * 70, fg='cyan'))
        
        for user in users:
            click.echo(f'{user.username:<20} {user.email:<30} {user.role:<10}')
        
        click.echo(click.style('─' * 70, fg='cyan'))
        
        # Print credentials note
        click.echo(click.style('\n📋 Default Credentials:', fg='cyan', bold=True))
        click.echo('Username: admin')
        click.echo('Password: admin123')


@cli.command()
@click.option('--limit', default=10, help='Number of recent alerts to show')
def show_alerts(limit):
    """Display recent alerts"""
    with app.app_context():
        alerts = Alert.query.order_by(Alert.created_at.desc()).limit(limit).all()
        
        if not alerts:
            click.echo(click.style('No alerts found', fg='yellow'))
            return
        
        click.echo(click.style(f'\n🚨 Recent Alerts (Last {limit}):', fg='cyan', bold=True))
        click.echo(click.style('─' * 80, fg='cyan'))
        
        for alert in alerts:
            txn = alert.transaction
            click.echo(f'\nAlert #{alert.id}')
            click.echo(f'  Transaction ID: {txn.transaction_id}')
            click.echo(f'  Amount: ${txn.amount:,.2f}')
            click.echo(f'  Sender → Receiver: {txn.sender_account} → {txn.receiver_account}')
            click.echo(f'  Risk Level: {click.style(alert.risk_level, fg="red", bold=True)}')
            click.echo(f'  Status: {alert.status}')
            click.echo(f'  Date: {alert.created_at.strftime("%Y-%m-%d %H:%M:%S")}')


if __name__ == '__main__':
    cli()
