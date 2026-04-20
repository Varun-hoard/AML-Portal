# AML SYSTEM - CORE ALGORITHMS

## 1. FRAUD DETECTION ALGORITHM

### Main Fraud Detection Flow

```
INPUT: New Transaction (sender, receiver, amount, date)
│
├─ Step 1: Extract Transaction Details
│   ├─ sender_account
│   ├─ receiver_account
│   ├─ amount
│   ├─ transaction_date
│   └─ currency
│
├─ Step 2: Initialize Risk Scoring
│   ├─ risk_score = 0
│   └─ triggered_rules = []
│
├─ Step 3: Apply Rule 1 - High Amount Check
│   IF amount > 10,000 THEN
│   │   risk_score += 30
│   │   triggered_rules.append("High Amount Detected")
│   ENDIF
│
├─ Step 4: Apply Rule 2 - Rapid Transaction Check
│   IF count(transactions from sender in last 60 minutes) >= 5 THEN
│   │   risk_score += 35
│   │   triggered_rules.append("Rapid Transactions")
│   ENDIF
│
├─ Step 5: Apply Rule 3 - Pattern Detection
│   IF count(sender→receiver pairs seen before) >= 3 THEN
│   │   risk_score += 25
│   │   triggered_rules.append("Repeated Pattern")
│   ENDIF
│
├─ Step 6: Apply Rule 4 - Suspicious Account Check
│   IF sender.startswith("SUSP_") OR receiver.startswith("SUSP_") THEN
│   │   risk_score += 40
│   │   triggered_rules.append("Suspicious Account")
│   ENDIF
│
├─ Step 7: Calculate Risk Level
│   IF risk_score >= 80 THEN
│   │   risk_level = "CRITICAL"
│   ELSE IF risk_score >= 50 THEN
│   │   risk_level = "HIGH"
│   ELSE IF risk_score >= 30 THEN
│   │   risk_level = "MEDIUM"
│   ELSE
│   │   risk_level = "LOW"
│   ENDIF
│
├─ Step 8: Determine if Suspicious
│   suspicious = (risk_score >= 30)
│
└─ OUTPUT: 
    {
      "is_suspicious": boolean,
      "risk_level": string,
      "risk_score": integer,
      "triggered_rules": array,
      "detection_reason": string
    }
```

---

## 2. PSEUDO CODE - Fraud Detection Function

```python
FUNCTION detectSuspiciousTransaction(transaction):
    
    # Initialize variables
    risk_score = 0
    triggered_rules = []
    
    # Rule 1: High Amount Detection
    IF transaction.amount > 10000:
        risk_score = risk_score + 30
        triggered_rules.push("High Amount Detected")
    END IF
    
    # Rule 2: Rapid Transactions Detection
    recent_txns = Database.query(
        FROM Transactions 
        WHERE sender = transaction.sender 
        AND created_at > (NOW - 60 minutes)
    )
    
    IF recent_txns.count() >= 5:
        risk_score = risk_score + 35
        triggered_rules.push("Rapid Transactions")
    END IF
    
    # Rule 3: Repeated Pattern Detection
    repeated_pairs = Database.query(
        FROM Transactions 
        WHERE sender = transaction.sender 
        AND receiver = transaction.receiver
    )
    
    IF repeated_pairs.count() >= 3:
        risk_score = risk_score + 25
        triggered_rules.push("Repeated Pattern")
    END IF
    
    # Rule 4: Suspicious Account Detection
    IF transaction.sender STARTSWITH "SUSP_" 
       OR transaction.receiver STARTSWITH "SUSP_":
        risk_score = risk_score + 40
        triggered_rules.push("Suspicious Account")
    END IF
    
    # Calculate Risk Level
    IF risk_score >= 80:
        risk_level = "CRITICAL"
    ELSE IF risk_score >= 50:
        risk_level = "HIGH"
    ELSE IF risk_score >= 30:
        risk_level = "MEDIUM"
    ELSE:
        risk_level = "LOW"
    END IF
    
    # Determine if Suspicious
    is_suspicious = (risk_score >= 30)
    
    RETURN {
        is_suspicious: is_suspicious,
        risk_level: risk_level,
        risk_score: risk_score,
        triggered_rules: triggered_rules,
        detection_reason: JOIN(triggered_rules, ", ")
    }
END FUNCTION
```

---

## 3. ALERT GENERATION ALGORITHM

```
INPUT: Detected Suspicious Transaction
│
├─ Step 1: Check if Alert Already Exists
│   IF Alert EXISTS for this transaction THEN
│   │   RETURN (Already recorded)
│   ENDIF
│
├─ Step 2: Create New Alert
│   alert = CREATE NEW Alert:
│   ├─ transaction_id = transaction.id
│   ├─ risk_level = transaction.risk_level
│   ├─ status = "OPEN"
│   ├─ triggered_rules = transaction.triggered_rules
│   ├─ analyst_notes = (empty)
│   ├─ created_at = NOW()
│   └─ updated_at = NOW()
│
├─ Step 3: Save Alert to Database
│   Database.INSERT(alert)
│
├─ Step 4: Log Alert Event
│   Logger.INFO("Alert created: ID=" + alert.id)
│
└─ OUTPUT: Alert created successfully
```

---

## 4. AUTHENTICATION ALGORITHM

### Login Flow

```
INPUT: username, password (from user login form)
│
├─ Step 1: Validate Input
│   IF username IS EMPTY OR password IS EMPTY THEN
│   │   RETURN ERROR (400: Missing credentials)
│   ENDIF
│
├─ Step 2: Find User in Database
│   user = Database.QUERY(
│       FROM Users 
│       WHERE username = input.username
│   )
│
├─ Step 3: Check if User Exists
│   IF user NOT FOUND THEN
│   │   Logger.WARNING("Failed login: unknown user")
│   │   RETURN ERROR (401: Invalid credentials)
│   ENDIF
│
├─ Step 4: Verify Password
│   stored_hash = user.password_hash
│   input_hash = HASH(input.password)
│   
│   IF stored_hash != input_hash THEN
│   │   RETURN ERROR (401: Invalid credentials)
│   ENDIF
│
├─ Step 5: Check Account Status
│   IF user.is_active == FALSE THEN
│   │   RETURN ERROR (403: Account inactive)
│   ENDIF
│
├─ Step 6: Create Session
│   session.user_id = user.id
│   user.last_login = NOW()
│   Database.UPDATE(user)
│
├─ Step 7: Log Success
│   Logger.INFO("User logged in: " + user.username)
│
└─ OUTPUT: 
    Session created
    Return user object
    Redirect to Dashboard
```

---

## 5. TRANSACTION CREATION ALGORITHM

```
INPUT: Transaction Details (sender, receiver, amount, currency, date)
│
├─ Step 1: Validate Input
│   FOR EACH required_field IN [sender, receiver, amount, currency, date]:
│   │   IF required_field IS EMPTY OR INVALID THEN
│   │   │   RETURN ERROR (400: Invalid input)
│   │   ENDIF
│   END FOR
│
├─ Step 2: Create Transaction Object
│   transaction = CREATE NEW Transaction:
│   ├─ transaction_id = GENERATE_UNIQUE_ID()
│   ├─ sender_account = input.sender
│   ├─ receiver_account = input.receiver
│   ├─ amount = input.amount
│   ├─ currency = input.currency
│   ├─ transaction_date = input.date
│   └─ created_at = NOW()
│
├─ Step 3: Save Transaction to Database
│   Database.INSERT(transaction)
│
├─ Step 4: Run Fraud Detection
│   detection_result = detectSuspiciousTransaction(transaction)
│   transaction.is_suspicious = detection_result.is_suspicious
│   transaction.risk_level = detection_result.risk_level
│   transaction.detection_reason = detection_result.detection_reason
│   Database.UPDATE(transaction)
│
├─ Step 5: Check if Alert Needed
│   IF detection_result.is_suspicious == TRUE THEN
│   │   CREATE NEW Alert:
│   │   ├─ transaction_id = transaction.id
│   │   ├─ risk_level = detection_result.risk_level
│   │   ├─ triggered_rules = detection_result.triggered_rules
│   │   └─ status = "OPEN"
│   │   Database.INSERT(alert)
│   │   Logger.INFO("Alert generated for transaction: " + transaction.id)
│   ENDIF
│
├─ Step 6: Log Success
│   Logger.INFO("Transaction created: " + transaction.id)
│
└─ OUTPUT: 
    Transaction saved
    Alert created (if suspicious)
    Return transaction object with alert status
```

---

## 6. PAGINATION ALGORITHM

```
INPUT: page_number, items_per_page, total_items
│
├─ Step 1: Validate Pagination Inputs
│   IF page_number < 1 THEN page_number = 1
│   IF items_per_page < 1 THEN items_per_page = 20
│   IF items_per_page > 100 THEN items_per_page = 100  // Limit max
│
├─ Step 2: Calculate Offset
│   offset = (page_number - 1) * items_per_page
│
├─ Step 3: Query Data with Limit/Offset
│   data = Database.QUERY(
│       SELECT * FROM table
│       ORDER BY created_at DESC
│       LIMIT items_per_page
│       OFFSET offset
│   )
│
├─ Step 4: Calculate Total Pages
│   total_pages = CEIL(total_items / items_per_page)
│
├─ Step 5: Validate Page Number
│   IF page_number > total_pages THEN
│   │   IF total_items > 0 THEN
│   │   │   page_number = total_pages
│   │   ELSE
│   │   │   page_number = 1
│   │   ENDIF
│   ENDIF
│
└─ OUTPUT: 
    {
      "items": data,
      "current_page": page_number,
      "total_pages": total_pages,
      "total_items": total_items,
      "has_next": (page_number < total_pages),
      "has_prev": (page_number > 1)
    }
```

---

## 7. DATA FILTERING ALGORITHM

### Alert Filter by Status

```
INPUT: alerts_list, filter_status
│
├─ Step 1: Validate Filter
│   valid_statuses = ["OPEN", "INVESTIGATING", "RESOLVED", "FALSE_POSITIVE"]
│   IF filter_status NOT IN valid_statuses THEN
│   │   RETURN alerts_list  // Return all if invalid
│   ENDIF
│
├─ Step 2: Filter Alerts
│   filtered_alerts = []
│   FOR EACH alert IN alerts_list:
│   │   IF alert.status == filter_status THEN
│   │   │   filtered_alerts.APPEND(alert)
│   │   ENDIF
│   END FOR
│
└─ OUTPUT: filtered_alerts
```

---

## 8. BULK UPDATE ALGORITHM

```
INPUT: alert_ids (array), update_data (object with status/notes)
│
├─ Step 1: Validate Input
│   IF alert_ids IS EMPTY THEN
│   │   RETURN ERROR (400: No alerts specified)
│   ENDIF
│   IF update_data IS EMPTY THEN
│   │   RETURN ERROR (400: No update data)
│   ENDIF
│
├─ Step 2: Initialize Counter
│   updated_count = 0
│
├─ Step 3: Loop Through Each Alert ID
│   FOR EACH alert_id IN alert_ids:
│   │   
│   │   ├─ Find Alert in Database
│   │   │  alert = Database.QUERY(FROM Alerts WHERE id = alert_id)
│   │   │
│   │   ├─ Check if Alert Exists
│   │   │  IF alert NOT FOUND THEN
│   │   │  │   CONTINUE TO NEXT ITERATION
│   │   │  ENDIF
│   │   │
│   │   ├─ Update Status (if provided)
│   │   │  IF "status" IN update_data THEN
│   │   │  │   alert.status = update_data.status
│   │   │  ENDIF
│   │   │
│   │   ├─ Update Notes (if provided)
│   │   │  IF "analyst_notes" IN update_data THEN
│   │   │  │   alert.analyst_notes = update_data.analyst_notes
│   │   │  ENDIF
│   │   │
│   │   ├─ Update Timestamp
│   │   │  alert.updated_at = NOW()
│   │   │
│   │   ├─ Save to Database
│   │   │  Database.UPDATE(alert)
│   │   │
│   │   └─ Increment Counter
│   │      updated_count = updated_count + 1
│   │
│   END FOR
│
├─ Step 4: Commit Transaction
│   Database.COMMIT()
│
├─ Step 5: Log Success
│   Logger.INFO("Bulk updated " + updated_count + " alerts")
│
└─ OUTPUT: 
    {
      "message": "Successfully updated X alerts",
      "updated_count": updated_count
    }
```

---

## 9. CSV EXPORT ALGORITHM

```
INPUT: data_type (transactions or alerts)
│
├─ Step 1: Query Data from Database
│   IF data_type == "transactions" THEN
│   │   data = Database.QUERY(SELECT * FROM Transactions)
│   │   columns = [ID, Sender, Receiver, Amount, Risk Level, ...]
│   ELSE IF data_type == "alerts" THEN
│   │   data = Database.QUERY(SELECT * FROM Alerts)
│   │   columns = [ID, Transaction ID, Risk Level, Status, ...]
│   ENDIF
│
├─ Step 2: Create CSV Structure
│   csv_file = CREATE_EMPTY_CSV()
│   csv_file.WRITE_HEADER(columns)
│
├─ Step 3: Write Data Rows
│   FOR EACH item IN data:
│   │   row = []
│   │   FOR EACH column IN columns:
│   │   │   value = item[column]
│   │   │   row.APPEND(ESCAPE_CSV(value))
│   │   END FOR
│   │   csv_file.WRITE_ROW(row)
│   END FOR
│
├─ Step 4: Generate Filename
│   timestamp = CURRENT_DATETIME()
│   filename = data_type + "_" + FORMATTED_DATE(timestamp) + ".csv"
│
├─ Step 5: Prepare Download
│   set_response_header("Content-Type", "text/csv")
│   set_response_header("Content-Disposition", "attachment; filename=" + filename)
│
└─ OUTPUT: 
    CSV file ready for download
    Browser triggers download
```

---

## 10. RISK CALCULATION ALGORITHM (DETAILED)

```
FUNCTION calculateRiskLevel(risk_score):
    
    IF risk_score >= 80:
        risk_level = "CRITICAL"
        color = "RED"
        severity = 4
        action = "IMMEDIATE INVESTIGATION"
    
    ELSE IF risk_score >= 50 AND risk_score < 80:
        risk_level = "HIGH"
        color = "ORANGE"
        severity = 3
        action = "PRIORITY INVESTIGATION"
    
    ELSE IF risk_score >= 30 AND risk_score < 50:
        risk_level = "MEDIUM"
        color = "YELLOW"
        severity = 2
        action = "REVIEW NEEDED"
    
    ELSE:  // risk_score < 30
        risk_level = "LOW"
        color = "GREEN"
        severity = 1
        action = "MONITOR"
    
    ENDIF
    
    RETURN {
        level: risk_level,
        score: risk_score,
        color: color,
        severity: severity,
        recommended_action: action
    }
    
END FUNCTION
```

---

## 11. DECISION TREE - FRAUD DETECTION

```
                    START: New Transaction
                          │
                          ▼
            ┌─────────────────────────────┐
            │ Check Amount > $10,000?      │
            └─────────────────────────────┘
              YES │                    │ NO
                  │                    │
              +30 │                    │
              ▼   │                    ▼
        ┌──────────────────────────────────────┐
        │ Check Rapid Transactions? (5 in 1h) │
        └──────────────────────────────────────┘
              YES │                    │ NO
                  │                    │
              +35 │                    │
              ▼   │                    ▼
        ┌──────────────────────────────────────┐
        │ Check Repeated Pattern? (3+ times)  │
        └──────────────────────────────────────┘
              YES │                    │ NO
                  │                    │
              +25 │                    │
              ▼   │                    ▼
        ┌──────────────────────────────────────┐
        │ Check Suspicious Account?            │
        └──────────────────────────────────────┘
              YES │                    │ NO
                  │                    │
              +40 │                    │
              ▼   │                    ▼
        ┌───────────────────────────────────────┐
        │ Total Risk Score                      │
        └───────────────────────────────────────┘
              │
              ├─ Score >= 30? → SUSPICIOUS (Alert)
              │
              ├─ Score >= 50? → HIGH Risk Alert
              │
              ├─ Score >= 80? → CRITICAL Alert
              │
              └─ Score < 30? → NORMAL (No Alert)
```

---

## 12. DATA FLOW DIAGRAM

```
User Input
    │
    ├─→ Login Request
    │       │
    │       ├─ Authenticate (Username + Password Hash)
    │       │
    │       └─ Session Created
    │
    └─→ Create Transaction
            │
            ├─ Validate Input
            │
            ├─ Save to Database
            │
            ├─ Run Fraud Detection (4 Rules)
            │
            ├─ Calculate Risk Score
            │
            ├─ Determine Risk Level
            │
            ├─ IF Suspicious (Risk >= 30)
            │   └─ Create Alert
            │
            └─ Return Result to User
                    │
                    ├─→ Dashboard (View Stats)
                    ├─→ Transactions (List/Filter)
                    ├─→ Alerts (View/Update)
                    └─→ Export (CSV Download)
```

---

## SUMMARY TABLE

| Algorithm | Input | Processing | Output |
|-----------|-------|-----------|--------|
| **Fraud Detection** | Transaction | Check 4 rules, calculate score | Risk level, suspicious flag |
| **Alert Generation** | Suspicious Txn | Create alert record | Alert object saved |
| **Authentication** | Username/Pwd | Hash & compare | Session or error |
| **Transaction Create** | Txn details | Validate, fraud check, save | Transaction + alert |
| **Pagination** | Page number | Calculate offset, query limit | Data page + metadata |
| **Filtering** | Data + filter | Filter by status/level | Filtered data |
| **Bulk Update** | Alert IDs + data | Loop and update each | Count updated |
| **CSV Export** | Data type | Query rows, format CSV | CSV file download |
| **Risk Calc** | Score | Map to level | Risk level object |

---

## KEY FORMULAS

### Fraud Detection Scoring
```
Total Risk Score = Sum of triggered rule points

Risk Level Mapping:
├─ CRITICAL:     80 ≤ score ≤ 130 (max = 30+35+25+40)
├─ HIGH:         50 ≤ score < 80
├─ MEDIUM:       30 ≤ score < 50
└─ LOW:          0 ≤ score < 30

Suspicious Alert Trigger: score >= 30
```

### Pagination
```
Offset = (page_number - 1) × items_per_page
Total_Pages = CEIL(total_items / items_per_page)
```

---

## TIME COMPLEXITY ANALYSIS

| Operation | Complexity | Notes |
|-----------|-----------|--------|
| Login | O(1) | Hash lookup, constant time |
| Create Transaction | O(n) | n = transactions in last 60 min |
| Fraud Detection | O(n) | n = database queries |
| List Alerts | O(k) | k = items on current page |
| Bulk Update | O(m) | m = number of alerts to update |
| CSV Export | O(n) | n = all items being exported |

