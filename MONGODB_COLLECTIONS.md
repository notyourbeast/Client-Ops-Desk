# MongoDB Collections Setup Guide

## Database Information

**Database Name:** `freelance_clienthub`  
**Connection:** Configured in `.env` file as `FCH_MONGO_URI`

## Collections Overview

Your application uses **5 collections** that are automatically created when you first use them:

### 1. `users`
**Purpose:** User accounts and authentication

**Fields:**
- `_id` (ObjectId) - Unique user ID
- `email` (String) - User email (unique)
- `password_hash` (String) - Hashed password
- `name` (String) - User's name
- `created_at` (DateTime) - Account creation date

**Indexes:**
- `email` (unique) - Fast login lookups
- `_id` - Primary key

---

### 2. `clients`
**Purpose:** Client information and contact details

**Fields:**
- `_id` (ObjectId) - Unique client ID
- `user_id` (ObjectId) - Owner user ID
- `name` (String) - Client name
- `email` (String) - Client email
- `phone` (String) - Client phone number
- `company` (String) - Company name
- `notes` (String) - Additional notes
- `created_at` (DateTime) - Creation date

**Indexes:**
- `user_id` - Fast queries for user's clients
- `email` - Search by email

---

### 3. `projects`
**Purpose:** Project details, status, and tracking

**Fields:**
- `_id` (ObjectId) - Unique project ID
- `user_id` (ObjectId) - Owner user ID
- `client_id` (ObjectId) - Associated client (optional)
- `title` (String) - Project title
- `description` (String) - Project description
- `status` (String) - Project status (idea, talks, in-progress, review, completed)
- `hourly_rate` (Float) - Hourly rate for billing
- `deadline` (DateTime) - Project deadline (optional)
- `created_at` (DateTime) - Creation date

**Indexes:**
- `user_id` - Fast queries for user's projects
- `client_id` - Fast queries for client's projects
- `status` - Filter by status

---

### 4. `invoices`
**Purpose:** Invoice records and payment tracking

**Fields:**
- `_id` (ObjectId) - Unique invoice ID
- `user_id` (ObjectId) - Owner user ID
- `project_id` (ObjectId) - Associated project
- `total_hours` (Float) - Total hours billed
- `amount_due` (Float) - Amount due
- `status` (String) - Invoice status (paid, unpaid)
- `due_date` (DateTime) - Payment due date
- `created_at` (DateTime) - Invoice creation date

**Indexes:**
- `user_id` - Fast queries for user's invoices
- `project_id` - Fast queries for project's invoices
- `status` - Filter by payment status
- `created_at` - Sort by date

---

### 5. `time_logs`
**Purpose:** Time tracking logs for projects

**Fields:**
- `_id` (ObjectId) - Unique log ID
- `user_id` (ObjectId) - Owner user ID
- `project_id` (ObjectId) - Associated project
- `start_time` (DateTime) - Timer start time
- `end_time` (DateTime) - Timer end time (null if running)
- `duration_minutes` (Integer) - Duration in minutes (null if running)
- `created_at` (DateTime) - Log creation date

**Indexes:**
- `user_id` - Fast queries for user's time logs
- `project_id` - Fast queries for project's time logs
- `start_time` - Sort by start time
- `end_time` - Filter active timers

---

## Setup Instructions

### Option 1: Automatic Setup (Recommended)

Run the setup script:

```bash
python setup_mongodb.py
```

This will:
- ✅ Connect to MongoDB
- ✅ Verify database exists
- ✅ Create collections (if needed)
- ✅ Create indexes for optimal performance
- ✅ Show collection statistics

### Option 2: Manual Setup

Collections are created automatically when you first insert data. However, you can verify everything is set up:

```bash
# Connect to MongoDB
mongosh

# Use your database
use freelance_clienthub

# Check collections
show collections

# View a collection
db.users.find().pretty()
```

### Option 3: Let Application Create Collections

**No action needed!** Collections are automatically created when you:
1. Register a user → creates `users` collection
2. Create a client → creates `clients` collection
3. Create a project → creates `projects` collection
4. Create an invoice → creates `invoices` collection
5. Start a timer → creates `time_logs` collection

## Indexes for Performance

Indexes are automatically created by the setup script. They improve query performance:

- **User-based queries** - All collections index `user_id` for fast user data retrieval
- **Relationships** - `client_id`, `project_id` indexes for joining data
- **Filtering** - `status`, `email` indexes for filtering
- **Sorting** - `created_at`, `start_time` indexes for date sorting

## Verification

After setup, verify everything works:

```bash
# Test connection
python -c "from app.repositories.db import get_db; db = get_db(); print('Database:', db.name)"

# Run setup script
python setup_mongodb.py

# Check collections in MongoDB shell
mongosh
use freelance_clienthub
show collections
```

## Collection Statistics

View collection statistics:

```bash
mongosh
use freelance_clienthub

# Count documents in each collection
db.users.countDocuments({})
db.clients.countDocuments({})
db.projects.countDocuments({})
db.invoices.countDocuments({})
db.time_logs.countDocuments({})

# View indexes
db.users.getIndexes()
db.clients.getIndexes()
```

## Important Notes

1. **Collections are created automatically** - No need to create them manually
2. **Indexes improve performance** - Run `setup_mongodb.py` to create them
3. **Data is user-scoped** - All queries filter by `user_id` for security
4. **Relationships** - Projects link to clients, invoices link to projects
5. **Time logs** - Track time spent on projects for invoice generation

## Next Steps

1. ✅ Run `python setup_mongodb.py` to set up indexes
2. ✅ Start your application: `python run.py`
3. ✅ Register a user account
4. ✅ Create some test data
5. ✅ Verify data in MongoDB using `mongosh`

---

**Ready to go!** Your MongoDB database is configured and ready to use. 🚀

