@echo off
REM AML System - Test Environment Setup & Run Script (Windows)

echo.
echo ==========================================
echo  AML SYSTEM - TEST ENVIRONMENT
echo ==========================================
echo.
echo Please choose an option:
echo.
echo 1. Run with Dummy Data (Recommended)
echo 2. Create Dummy Data + Run
echo 3. Clear All Data
echo 4. View Statistics
echo 5. Show Users
echo 6. Reset Database
echo 7. Exit
echo.

set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" goto run_test
if "%choice%"=="2" goto seed_and_run
if "%choice%"=="3" goto clear_data
if "%choice%"=="4" goto show_stats
if "%choice%"=="5" goto show_users
if "%choice%"=="6" goto reset_db
if "%choice%"=="7" goto end
goto invalid

:run_test
echo.
echo Starting AML System with dummy data...
echo.
python run_test.py
goto end

:seed_and_run
echo.
set /p count="Number of transactions (default 150): "
if "%count%"=="" set count=150

echo Seeding database with %count% transactions...
python manage.py seed-db --count %count%

echo.
echo Starting Flask application...
python app.py
goto end

:clear_data
echo.
echo WARNING: This will delete ALL transactions and alerts!
set /p confirm="Are you sure? (yes/no): "
if /i "%confirm%"=="yes" (
    python manage.py clear-db
    echo Database cleared!
) else (
    echo Cancelled.
)
goto menu

:show_stats
echo.
python manage.py show-stats
pause
goto menu

:show_users
echo.
python manage.py show-users
pause
goto menu

:reset_db
echo.
echo WARNING: This will reset the entire database!
set /p confirm="Are you sure? (yes/no): "
if /i "%confirm%"=="yes" (
    python manage.py reset-db
    echo Database reset complete!
    python manage.py show-users
) else (
    echo Cancelled.
)
goto menu

:menu
echo.
pause
cls
goto start

:invalid
echo Invalid choice!
pause
cls
goto start

:end
echo.
echo Goodbye!
echo.
pause
