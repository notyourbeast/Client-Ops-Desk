# 📋 Complete Project Workflow & Architecture

## 🎯 Project Overview

**Freelance Client Hub** - A full-stack web application for freelancers to manage clients, projects, time tracking, and invoicing.

---

## 🏗️ Architecture Overview

### **Technology Stack**

```
Frontend:     HTML5, CSS3 (Tailwind CSS), JavaScript (Vanilla)
Backend:      Python 3.x, Flask (Web Framework)
Database:     MongoDB (NoSQL Document Database)
Authentication: JWT (JSON Web Tokens) + Google OAuth 2.0
Deployment:   Render (Backend), Netlify (Frontend - if needed)
Server:       Gunicorn (Production WSGI Server)
```

### **Project Structure**

```
app/
├── __init__.py              # Application factory, OAuth setup
├── config.py                # Configuration management
├── models/                  # Data models
├── repositories/            # Database access layer
│   ├── db.py               # MongoDB connection
│   ├── client_repository.py
│   ├── project_repository.py
│   ├── invoice_repository.py
│   └── time_log_repository.py
├── services/                # Business logic layer
│   ├── auth_service.py
│   ├── client_service.py
│   ├── project_service.py
│   ├── invoice_service.py
│   ├── time_log_service.py
│   └── search_service.py
├── routes/                  # HTTP request handlers
│   ├── auth_routes.py
│   ├── client_routes.py
│   ├── project_routes.py
│   ├── invoice_routes.py
│   ├── time_routes.py
│   └── search_routes.py
├── templates/              # Jinja2 HTML templates
│   ├── base.html           # Base template with AJAX
│   ├── dashboard.html
│   ├── clients/
│   ├── projects/
│   ├── invoices/
│   └── search/
└── utils/                   # Utilities
    ├── auth_decorators.py  # @login_required decorator
    └── jwt_utils.py        # JWT token management
```

---

## 🔄 Request Flow Architecture

### **3-Layer Architecture**

```
┌─────────────────────────────────────────────────────────┐
│                    CLIENT (Browser)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐│
│  │   HTML/CSS   │  │  JavaScript   │  │   AJAX/Fetch ││
│  └──────────────┘  └──────────────┘  └──────────────┘│
└───────────────────────────┬─────────────────────────────┘
                            │ HTTP Request
                            ▼
┌─────────────────────────────────────────────────────────┐
│              ROUTES LAYER (Flask Blueprints)              │
│  • Receives HTTP requests                               │
│  • Validates authentication (@login_required)            │
│  • Extracts form/query parameters                        │
│  • Calls service layer                                   │
│  • Returns HTML/JSON responses                           │
└───────────────────────────┬─────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│            SERVICE LAYER (Business Logic)                 │
│  • Validates business rules                              │
│  • Orchestrates data operations                           │
│  • Calls repository layer                                │
│  • Handles calculations (invoice amounts, time totals)   │
└───────────────────────────┬─────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│         REPOSITORY LAYER (Database Access)               │
│  • Direct MongoDB operations                             │
│  • CRUD operations (Create, Read, Update, Delete)        │
│  • Query building                                        │
│  • Data transformation                                   │
└───────────────────────────┬─────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│              MONGODB DATABASE                            │
│  Collections: users, clients, projects, invoices,       │
│               time_logs                                  │
└─────────────────────────────────────────────────────────┘
```

---

## 🔐 Authentication Flow

### **1. User Registration (Traditional)**

```
User → /auth/register (GET)
     → Renders registration form
     → User submits form (POST)
     → auth_routes.register()
     → auth_service.register_user()
     → Repository creates user in MongoDB
     → Password hashed with bcrypt
     → Redirects to login
```

### **2. User Login (Traditional)**

```
User → /auth/login (GET)
     → Renders login form
     → User submits credentials (POST)
     → auth_routes.login()
     → auth_service.authenticate_user()
     → Repository queries MongoDB for user
     → Verifies password hash
     → jwt_utils.create_token() generates JWT
     → Sets HTTP-only cookie: auth_token
     → Stores user info in Flask session
     → Redirects to /dashboard
```

### **3. Google OAuth Login**

```
User → Clicks "Continue with Google"
     → /auth/google/login (GET)
     → Redirects to Google OAuth consent screen
     → User authorizes app
     → Google redirects to /auth/google/callback
     → auth_routes.google_callback()
     → Fetches user info from Google API
     → oauth_service.get_or_create_google_user()
     → Creates user if doesn't exist
     → Stores Google profile picture in session
     → Generates JWT token
     → Sets cookie and redirects to dashboard
```

### **4. Protected Route Access**

```
User → Accesses protected route (e.g., /clients)
     → @login_required decorator intercepts
     → Reads auth_token from cookie
     → jwt_utils.decode_token() validates JWT
     → Queries MongoDB for user
     → Sets g.current_user
     → Route handler executes
```

---

## 📊 Core Workflows

### **Workflow 1: Client Management**

```
1. CREATE CLIENT
   User → /clients (GET) → Shows client list
   → Clicks "Add Client"
   → Fills form → Submits (POST)
   → client_routes.create_client()
   → client_service.create_client_for_user()
   → client_repository.create_client()
   → MongoDB: Insert into 'clients' collection
   → Redirects to client list

2. LIST CLIENTS (with AJAX)
   User → /clients (GET)
   → client_routes.list_clients()
   → Fetches all clients for user
   → Applies search/filter (if provided)
   → Renders template
   
   If AJAX request (X-Requested-With header):
   → Returns partial HTML (_results_table.html)
   → JavaScript replaces only results container
   → No page reload!

3. SEARCH/FILTER CLIENTS
   User → Types in search box
   → JavaScript intercepts form submission
   → Sends AJAX request with query params
   → Server returns filtered results
   → Updates URL with History API
   → Replaces results table only
```

### **Workflow 2: Project Management**

```
1. CREATE PROJECT
   User → /projects (GET)
   → Selects client (optional)
   → Fills project details (title, status, hourly rate, deadline)
   → Submits form
   → project_routes.create_project()
   → project_service.create_project_for_user()
   → project_repository.create_project()
   → MongoDB: Insert into 'projects' collection
   → Links to client via client_id

2. UPDATE PROJECT STATUS
   User → Changes status dropdown
   → JavaScript sends AJAX POST to /projects/<id>/status
   → project_routes.update_status()
   → Updates status in MongoDB
   → Returns JSON success
   → UI updates without reload

3. TIME TRACKING
   User → Clicks "Start" button on project
   → JavaScript POST to /projects/<id>/start-timer
   → time_routes.start_timer()
   → time_log_repository.start_timer()
   → MongoDB: Creates time_log with start_time, end_time=null
   → Returns start_time
   → JavaScript updates UI (shows timer, hides Start button)
   
   User → Clicks "Stop" button
   → JavaScript POST to /projects/<id>/stop-timer
   → time_routes.stop_timer()
   → time_log_repository.stop_timer()
   → MongoDB: Updates time_log with end_time and duration_minutes
   → Calculates: duration = end_time - start_time
   → Returns duration
   → JavaScript updates UI
```

### **Workflow 3: Invoice Generation**

```
1. CREATE INVOICE
   User → /invoices (GET)
   → Selects project from dropdown
   → Sets due date
   → Submits form
   → invoice_routes.create_invoice()
   → invoice_service.create_invoice_for_project()
   → Fetches project (to get hourly_rate)
   → Fetches all time_logs for project
   → Calculates:
      • total_hours = sum(duration_minutes) / 60
      • amount_due = total_hours × hourly_rate
   → invoice_repository.create_invoice()
   → MongoDB: Insert into 'invoices' collection
   → Redirects to invoice list

2. MARK INVOICE AS PAID
   User → Clicks "Mark Paid" button
   → JavaScript POST to /invoices/<id>/mark-paid
   → invoice_routes.mark_paid()
   → invoice_repository.mark_invoice_paid()
   → MongoDB: Updates invoice status to 'paid'
   → Returns JSON success
   → JavaScript removes "Mark Paid" button
```

### **Workflow 4: Dashboard Metrics**

```
User → /dashboard (GET)
→ @login_required validates authentication
→ dashboard() function in __init__.py

METRICS CALCULATED:

1. Total Clients
   → client_service.get_user_clients()
   → Counts all clients for user

2. Active Projects
   → project_service.get_user_projects()
   → Filters: status != 'completed'
   → Counts active projects

3. Monthly Hours
   → Queries time_logs collection
   → Filters: end_time >= first_day_of_month
   → Sums duration_minutes, converts to hours

4. Weekly Hours Breakdown
   → Groups monthly logs by week
   → Calculates hours per week (5 weeks)
   → Used for bar chart visualization

5. Unpaid Invoices
   → invoice_service.get_user_invoices()
   → Filters: status == 'unpaid'
   → Counts and sums amount_due

6. Monthly Revenue
   → Filters invoices: status == 'paid' AND created_at >= first_day_of_month
   → Sums amount_due

7. Top Projects (by hours)
   → Groups time_logs by project_id
   → Sums hours per project
   → Sorts descending, takes top 3

→ Renders dashboard.html with metrics
```

### **Workflow 5: Global Search**

```
User → Types in header search box
→ Presses Enter
→ JavaScript checks if on /search page
   • If YES: AJAX request to /search?q=query
   • If NO: Navigate to /search?q=query

→ search_routes.search_results()
→ search_service.search_all()
→ Searches across:
   • Clients: name, company, email, phone
   • Projects: title, description
   • Invoices: project_name, amount, status
→ Returns combined results
→ Renders search/results.html
```

---

## 🗄️ Database Schema

### **MongoDB Collections**

#### **1. users**
```javascript
{
  _id: ObjectId,
  email: String (unique),
  password_hash: String (bcrypt),
  name: String,
  created_at: DateTime,
  google_id: String (optional, for OAuth users)
}
```

#### **2. clients**
```javascript
{
  _id: ObjectId,
  user_id: ObjectId,
  name: String,
  email: String,
  phone: String,
  company: String,
  notes: String,
  created_at: DateTime
}
```

#### **3. projects**
```javascript
{
  _id: ObjectId,
  user_id: ObjectId,
  client_id: ObjectId (optional),
  title: String,
  description: String,
  status: String (idea, talks, in-progress, review, completed),
  hourly_rate: Float,
  deadline: DateTime,
  created_at: DateTime
}
```

#### **4. invoices**
```javascript
{
  _id: ObjectId,
  user_id: ObjectId,
  project_id: ObjectId,
  total_hours: Float,
  amount_due: Float,
  status: String (paid, unpaid),
  due_date: DateTime,
  created_at: DateTime
}
```

#### **5. time_logs**
```javascript
{
  _id: ObjectId,
  user_id: ObjectId,
  project_id: ObjectId,
  start_time: DateTime,
  end_time: DateTime (null if active),
  duration_minutes: Integer (null if active),
  created_at: DateTime
}
```

**Indexes:**
- All collections have indexes on `user_id` for fast queries
- `projects.client_id` indexed for client filtering
- `time_logs.project_id` indexed for project time aggregation

---

## 🔄 AJAX Implementation Details

### **How AJAX Search/Filter Works**

```
1. USER ACTION
   User types in search box → Clicks "Filter"
   
2. JAVASCRIPT INTERCEPTION
   Form submit event → e.preventDefault()
   → Extracts form data
   → Builds URL with query params
   
3. AJAX REQUEST
   fetch(url, {
     headers: { 'X-Requested-With': 'XMLHttpRequest' }
   })
   
4. SERVER DETECTION
   Route handler checks: request.headers.get('X-Requested-With')
   → If 'XMLHttpRequest': Returns partial template
   → If not: Returns full page template
   
5. CLIENT UPDATE
   Receives partial HTML
   → Replaces container.innerHTML
   → Updates URL: window.history.pushState()
   → Re-initializes scripts (timers, etc.)
   
6. NO PAGE RELOAD
   Only results section updates
   → Much faster user experience
```

### **Browser History Support**

```
User clicks browser back button
→ popstate event fires
→ JavaScript detects current path
→ Determines which container to update
→ Sends AJAX request with current URL
→ Updates results without full reload
```

---

## 🚀 Application Startup Flow

```
1. run.py executed
   → Imports create_app() from app/__init__.py
   
2. create_app() called
   → Creates Flask app instance
   → Loads Config from environment variables
   → Sets up ProxyFix middleware (for Render deployment)
   → Initializes Google OAuth (if credentials provided)
   → Registers all blueprints (routes)
   → Defines dashboard route
   → Returns app instance
   
3. Gunicorn starts (production)
   → Runs: gunicorn run:app
   → Listens on PORT environment variable
   → Handles multiple requests
   
4. MongoDB Connection
   → First database operation triggers connection
   → get_db() called
   → get_client() creates MongoClient
   → Tests connection with ping()
   → Returns database instance
```

---

## 🔒 Security Features

1. **JWT Authentication**
   - Tokens stored in HTTP-only cookies
   - Prevents XSS attacks
   - Expires after 7 days

2. **Password Hashing**
   - bcrypt used for password storage
   - Never stored in plain text

3. **OAuth 2.0**
   - Google handles authentication
   - No password storage for OAuth users

4. **User Isolation**
   - All queries filtered by user_id
   - Users can only access their own data

5. **HTTPS Support**
   - ProxyFix middleware detects HTTPS
   - Required for production OAuth

---

## 📱 User Interface Features

1. **Responsive Design**
   - Tailwind CSS for styling
   - Mobile-friendly layouts
   - Sidebar navigation

2. **AJAX Enhancements**
   - No page reloads for search/filter
   - Instant updates
   - Loading indicators

3. **Real-time Timers**
   - JavaScript updates timer display every second
   - Shows elapsed time for active timers

4. **Interactive Elements**
   - Status dropdowns update via AJAX
   - Delete confirmations
   - Flash messages for feedback

---

## 🎯 Key Design Patterns

1. **Repository Pattern**
   - Separates database logic from business logic
   - Easy to swap database implementations

2. **Service Layer Pattern**
   - Business logic in services
   - Routes only handle HTTP concerns

3. **Blueprint Pattern**
   - Modular route organization
   - Each feature in separate blueprint

4. **Decorator Pattern**
   - @login_required for authentication
   - Reusable across routes

5. **Factory Pattern**
   - create_app() factory function
   - Enables testing and multiple instances

---

## 🔧 Environment Configuration

### **Required Environment Variables**

```bash
# Database
FCH_MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/
FCH_DB_NAME=freelance_clienthub

# Security
FCH_SECRET_KEY=your-secret-key
FCH_JWT_SECRET_KEY=your-jwt-secret

# Google OAuth (optional)
FCH_GOOGLE_CLIENT_ID=your-client-id
FCH_GOOGLE_CLIENT_SECRET=your-client-secret

# Production (Render)
FCH_SERVER_NAME=your-app.onrender.com
FCH_URL_SCHEME=https
PORT=10000
```

---

## 📈 Data Flow Example: Creating an Invoice

```
1. USER ACTION
   User selects project → Sets due date → Clicks "Create Invoice"

2. HTTP REQUEST
   POST /invoices
   Form data: { project_id: "...", due_date: "2024-01-15" }

3. ROUTE HANDLER
   invoice_routes.create_invoice()
   → Extracts user_id from g.current_user
   → Extracts form data
   → Calls service

4. SERVICE LAYER
   invoice_service.create_invoice_for_project()
   → Validates project exists
   → Checks project has hourly_rate
   → Fetches all time_logs for project
   → Calculates:
      total_hours = sum(time_logs.duration_minutes) / 60
      amount_due = total_hours × project.hourly_rate
   → Calls repository

5. REPOSITORY LAYER
   invoice_repository.create_invoice()
   → Builds invoice document
   → Inserts into MongoDB 'invoices' collection
   → Returns invoice document

6. RESPONSE
   → Service returns invoice
   → Route sets flash message
   → Redirects to /invoices
   → User sees new invoice in list
```

---

## 🎨 Frontend-Backend Communication

### **Traditional Form Submission**
```
HTML Form → POST request → Server processes → Redirect → Full page reload
```

### **AJAX Form Submission**
```
HTML Form → JavaScript intercepts → Fetch API → Server returns partial HTML
→ JavaScript updates DOM → No page reload
```

### **JSON API Endpoints**
```
JavaScript → Fetch API → Server returns JSON → JavaScript updates UI
(Used for timers, status updates, delete operations)
```

---

## 🐛 Error Handling

1. **Database Errors**
   - Connection failures caught
   - User-friendly error messages
   - Fallback to error pages

2. **Authentication Errors**
   - Invalid tokens redirect to login
   - Expired tokens handled gracefully

3. **Validation Errors**
   - Form validation on client and server
   - Flash messages for feedback

4. **AJAX Errors**
   - Network errors fall back to normal navigation
   - Loading states prevent duplicate requests

---

## 🚢 Deployment Flow

### **Production (Render)**

```
1. Code pushed to Git repository
2. Render detects changes
3. Builds application:
   → Installs dependencies from requirements.txt
   → Runs gunicorn run:app
4. Application starts on PORT environment variable
5. MongoDB Atlas connection established
6. Application ready to serve requests
```

### **Environment Setup on Render**

```
1. Add environment variables in Render dashboard
2. Set FCH_MONGO_URI (MongoDB Atlas connection string)
3. Set FCH_GOOGLE_CLIENT_ID and SECRET
4. Set FCH_SERVER_NAME and FCH_URL_SCHEME
5. Deploy
```

---

## 📊 Summary

This application follows a **clean 3-layer architecture**:

- **Routes** handle HTTP requests/responses
- **Services** contain business logic
- **Repositories** handle database operations

**Key Features:**
- ✅ User authentication (JWT + Google OAuth)
- ✅ Client management
- ✅ Project management with status tracking
- ✅ Time tracking with timers
- ✅ Invoice generation from time logs
- ✅ Dashboard with metrics
- ✅ Global search across entities
- ✅ AJAX-enhanced UI (no page reloads)
- ✅ Responsive design

**Data Flow:**
User → Route → Service → Repository → MongoDB → Response → User

**Security:**
- JWT tokens in HTTP-only cookies
- User data isolation
- Password hashing
- OAuth 2.0 integration

This architecture ensures **separation of concerns**, **maintainability**, and **scalability**.

