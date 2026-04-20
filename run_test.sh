#!/bin/bash
# AML System - Test Environment Setup & Run Script (Mac/Linux)

show_menu() {
    echo ""
    echo "=========================================="
    echo "  AML SYSTEM - TEST ENVIRONMENT"
    echo "=========================================="
    echo ""
    echo "Please choose an option:"
    echo ""
    echo "1. Run with Dummy Data (Recommended)"
    echo "2. Create Dummy Data + Run"
    echo "3. Clear All Data"
    echo "4. View Statistics"
    echo "5. Show Users"
    echo "6. Show Recent Alerts"
    echo "7. Reset Database"
    echo "8. Exit"
    echo ""
    read -p "Enter your choice (1-8): " choice
    
    case $choice in
        1) run_test ;;
        2) seed_and_run ;;
        3) clear_data ;;
        4) show_stats ;;
        5) show_users ;;
        6) show_alerts ;;
        7) reset_db ;;
        8) exit_menu ;;
        *) echo "Invalid choice!"; show_menu ;;
    esac
}

run_test() {
    echo ""
    echo "🧪 Starting AML System with dummy data..."
    echo ""
    python run_test.py
}

seed_and_run() {
    echo ""
    read -p "Number of transactions (default: 150): " count
    count=${count:-150}
    
    echo "🌱 Seeding database with $count transactions..."
    python manage.py seed-db --count $count
    
    echo ""
    echo "🚀 Starting Flask application..."
    python app.py
}

clear_data() {
    echo ""
    echo "⚠️  WARNING: This will delete ALL transactions and alerts!"
    read -p "Are you sure? (yes/no): " confirm
    
    if [ "$confirm" = "yes" ] || [ "$confirm" = "y" ]; then
        python manage.py clear-db
        echo "✅ Database cleared!"
    else
        echo "Cancelled."
    fi
    show_menu
}

show_stats() {
    echo ""
    python manage.py show-stats
    read -p "Press Enter to continue..."
    show_menu
}

show_users() {
    echo ""
    python manage.py show-users
    read -p "Press Enter to continue..."
    show_menu
}

show_alerts() {
    echo ""
    read -p "Number of alerts to show (default: 10): " limit
    limit=${limit:-10}
    python manage.py show-alerts --limit $limit
    read -p "Press Enter to continue..."
    show_menu
}

reset_db() {
    echo ""
    echo "⚠️  WARNING: This will reset the entire database!"
    read -p "Are you sure? (yes/no): " confirm
    
    if [ "$confirm" = "yes" ] || [ "$confirm" = "y" ]; then
        python manage.py reset-db
        echo "✅ Database reset complete!"
        python manage.py show-users
    else
        echo "Cancelled."
    fi
    show_menu
}

exit_menu() {
    echo ""
    echo "👋 Goodbye!"
    echo ""
    exit 0
}

# Main
show_menu
