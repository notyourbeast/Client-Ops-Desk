# Deploy Frontend to Netlify

**Important Note:** Your current application is a Flask app with server-side rendered templates. To deploy a frontend on Netlify, you have two options:

1. **Option A:** Keep everything on Render (recommended for your current setup)
2. **Option B:** Create a separate frontend that calls your Render API

This guide covers **Option B** - creating a separate frontend for Netlify.

---

## Prerequisites

- Render deployment completed (see DEPLOY_RENDER.md)
- Node.js installed (for building frontend)
- Netlify account (sign up at https://netlify.com)
- GitHub account

---

## Option A: Keep Everything on Render (Recommended)

Since your Flask app serves both API and templates, the simplest approach is to deploy everything on Render. Your app will be accessible at `https://your-app.onrender.com`.

**No additional steps needed if you choose this option.**

---

## Option B: Separate Frontend + Backend

If you want a separate frontend on Netlify, you'll need to:

1. Create a frontend application (React, Vue, or static HTML/JS)
2. Convert Flask routes to API endpoints
3. Deploy frontend to Netlify
4. Configure CORS

This is a significant refactoring. Below is a guide for this approach.

---

## Step 1: Create API Endpoints in Flask

### 1.1 Create API Blueprint

Create `app/routes/api_routes.py`:

```python
from flask import Blueprint, jsonify, request, g
from app.utils.auth_decorators import login_required
from app.services.client_service import get_user_clients, create_client_for_user
from app.services.project_service import get_user_projects, create_project_for_user
from app.services.invoice_service import get_user_invoices, create_invoice_for_project
from app.services.time_log_service import get_all_user_time_logs

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/clients', methods=['GET'])
@login_required
def get_clients():
    user_id = str(g.current_user['_id'])
    clients = get_user_clients(user_id)
    return jsonify([{
        '_id': str(c['_id']),
        'name': c.get('name'),
        'email': c.get('email'),
        'company': c.get('company'),
        'phone': c.get('phone'),
        'created_at': c.get('created_at').isoformat() if c.get('created_at') else None
    } for c in clients])

@api_bp.route('/clients', methods=['POST'])
@login_required
def create_client():
    user_id = str(g.current_user['_id'])
    data = request.json
    client, error = create_client_for_user(user_id, data)
    if error:
        return jsonify({'error': error}), 400
    return jsonify({
        '_id': str(client['_id']),
        'name': client.get('name'),
        'email': client.get('email'),
        'company': client.get('company'),
        'phone': client.get('phone')
    }), 201

# Add more API endpoints for projects, invoices, etc.
```

### 1.2 Register API Blueprint

In `app/__init__.py`:

```python
from .routes.api_routes import api_bp

# ... existing code ...

app.register_blueprint(api_bp)
```

### 1.3 Enable CORS

Add to `requirements.txt`:
```
flask-cors==4.0.0
```

In `app/__init__.py`:
```python
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    # ... existing code ...
    
    # Enable CORS for API routes
    CORS(app, resources={r"/api/*": {"origins": ["https://your-netlify-app.netlify.app"]}})
    
    return app
```

---

## Step 2: Create Frontend Application

### 2.1 Choose Frontend Framework

Options:
- **React** (recommended)
- **Vue.js**
- **Vanilla JavaScript**

### 2.2 Example: React Frontend Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── ClientList.js
│   │   ├── ProjectList.js
│   │   └── InvoiceList.js
│   ├── services/
│   │   └── api.js
│   ├── App.js
│   └── index.js
├── package.json
└── netlify.toml
```

### 2.3 Create API Service

`src/services/api.js`:

```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://your-app.onrender.com/api';

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const token = localStorage.getItem('auth_token');
    
    const config = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
        ...options.headers,
      },
    };

    const response = await fetch(url, config);
    
    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`);
    }
    
    return response.json();
  }

  // Clients
  async getClients() {
    return this.request('/clients');
  }

  async createClient(data) {
    return this.request('/clients', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Projects
  async getProjects() {
    return this.request('/projects');
  }

  async createProject(data) {
    return this.request('/projects', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Invoices
  async getInvoices() {
    return this.request('/invoices');
  }

  async createInvoice(data) {
    return this.request('/invoices', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
}

export default new ApiService();
```

---

## Step 3: Configure Netlify

### 3.1 Create netlify.toml

In your frontend project root:

```toml
[build]
  command = "npm run build"
  publish = "build"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[build.environment]
  REACT_APP_API_URL = "https://your-app.onrender.com/api"
```

### 3.2 Environment Variables

In Netlify dashboard:
- Go to **Site settings** → **Environment variables**
- Add: `REACT_APP_API_URL=https://your-app.onrender.com/api`

---

## Step 4: Deploy to Netlify

### 4.1 Via Netlify Dashboard

1. Go to https://app.netlify.com
2. Click **Add new site** → **Import an existing project**
3. Connect to GitHub
4. Select your frontend repository
5. Configure:
   - **Build command**: `npm run build`
   - **Publish directory**: `build`
6. Click **Deploy site**

### 4.2 Via Netlify CLI

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Deploy
netlify deploy --prod
```

---

## Step 5: Update OAuth Redirect URIs

### 5.1 Update Google Console

1. Go to Google Cloud Console
2. Update **Authorized JavaScript origins**:
   - Add: `https://your-netlify-app.netlify.app`
3. Update **Authorized redirect URIs**:
   - Add: `https://your-netlify-app.netlify.app/auth/callback`

### 5.2 Update Render Environment Variables

In Render dashboard, update:
- `FCH_SERVER_NAME=your-app.onrender.com` (keep this for API)
- Add CORS origins to include Netlify URL

---

## Step 6: Handle Authentication

### 6.1 Frontend Auth Flow

```javascript
// Login
const response = await fetch('https://your-app.onrender.com/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email, password }),
  credentials: 'include',
});

const data = await response.json();
if (data.token) {
  localStorage.setItem('auth_token', data.token);
}
```

### 6.2 Protected Routes

```javascript
// Check if user is authenticated
const token = localStorage.getItem('auth_token');
if (!token) {
  window.location.href = '/login';
}
```

---

## Alternative: Static Site with Netlify Functions

If you want to keep it simple, you can:

1. Deploy static HTML/JS to Netlify
2. Use Netlify Functions for serverless API calls
3. Keep MongoDB connection in Netlify Functions

This requires rewriting your Flask routes as Netlify Functions.

---

## Recommendation

**For your current Flask application, I recommend:**

✅ **Deploy everything on Render** (simpler, faster)
- Your Flask app already serves templates
- No need to separate frontend/backend
- Single deployment
- Easier to maintain

❌ **Separate frontend on Netlify** (more complex)
- Requires significant refactoring
- Need to create API endpoints
- Need to handle CORS
- More complex authentication flow
- Two deployments to manage

---

## Quick Start: Render Only

If you want to deploy everything on Render:

1. Follow **DEPLOY_RENDER.md**
2. Your app will be at `https://your-app.onrender.com`
3. All features work as-is
4. No Netlify needed

---

**Need help?** Choose the approach that fits your needs:
- **Simple**: Deploy everything on Render
- **Complex**: Separate frontend/backend (requires refactoring)

