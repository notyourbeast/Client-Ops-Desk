#Client Hub

A full-stack web application designed to help freelancers manage their client relationships, track project progress, log billable hours, and generate invoices. The application provides a centralized dashboard for monitoring business metrics and streamlines the workflow from client onboarding to payment collection. 

## Project Overview 
Freelance Client Hub addresses the common challenge of managing multiple clients, projects, and billing cycles without relying on disparate tools. The application consolidates client information, project tracking, time logging, and invoice generation into a single platform. 
 
 The architecture follows a three-layer pattern: routes handle HTTP requests and responses, services contain business logic, and repositories manage database operations. This separation ensures maintainability and testability while keeping concerns properly isolated. 
 
The application uses server-side rendering with Flask templates, enhanced with AJAX for dynamic updates without full page reloads. Authentication is handled through JWT tokens stored in HTTP-only cookies, with optional Google OAuth integration for streamlined login. 
 
## Features 
### Client Management 
 
Clients can be created, edited, and deleted. Each client record stores contact information including name, email, phone, company affiliation, and optional notes. The client list supports search across all fields and filtering by company name. Client details pages display associated projects and provide quick navigation to related invoices. 
 
### Project Management 
 
Projects track work items with status progression through five stages: idea, talks, in-progress, review, and completed. Each project can be associated with a client and includes an hourly rate for billing calculations. Projects support deadline tracking and detailed descriptions. Status updates occur via AJAX without page reloads, and the project list can be filtered by client or status. 
 
### Time Tracking 
 
Each project includes a built-in timer that tracks billable hours. Users can start and stop timers directly from the project list or detail pages. Active timers display elapsed time in real-time, updating every second. When stopped, the time is logged to the database with start and end timestamps, and the duration is calculated automatically. Only one timer can be active per user at any time. 
 
### Invoice Generation 
 
Invoices are generated from completed time logs for a specific project. The system calculates total billable hours from all time logs associated with the project and multiplies by the project's hourly rate to determine the amount due. Invoices can be marked as paid or unpaid, and the dashboard aggregates unpaid invoice totals. Each invoice includes a due date and links back to its source project. 
 
### Dashboard Analytics 
 
The dashboard provides an overview of business metrics including total clients, active projects, monthly hours logged, weekly hour breakdowns, unpaid invoice counts and amounts, monthly revenue from paid invoices, and top three projects by hours logged. Metrics are calculated in real-time from the database and displayed with visual charts for weekly hours. 
 
### Global Search 
 
A unified search interface allows users to search across clients, projects, and invoices simultaneously. Search results are grouped by entity type and display relevant information with links to detail pages. The search interface supports AJAX updates to avoid page reloads. 
 
### AJAX-Enhanced Interface 
 
All list views support AJAX-based filtering and searching. Form submissions are intercepted by JavaScript, which sends requests with an X-Requested-With header. The server detects these requests and returns partial HTML templates containing only the results table. The client-side JavaScript updates the DOM and uses the History API to update the URL without triggering a full page reload. This provides a faster, more responsive user experience while maintaining browser history support. 
 
## Technical Stack 
 
### Frontend 
 
- **HTML5**: Semantic markup for all pages 
- **CSS3 with Tailwind CSS**: Utility-first CSS framework for responsive design 
- **JavaScript (Vanilla)**: No frameworks, pure JavaScript for AJAX interactions, timer updates, and form handling 
- **Jinja2 Templates**: Server-side templating engine integrated with Flask 
 
### Backend 
 
- **Python 3.x**: Core programming language 
- **Flask 3.0.0**: Web framework handling routing, request/response cycle, and template rendering 
- **Gunicorn 21.2.0**: Production WSGI server for deployment 
 
### Database 
 
- **MongoDB**: NoSQL document database for flexible schema 
- **PyMongo 4.6.0**: Official MongoDB driver for Python 
- **MongoDB Atlas**: Cloud-hosted database option with connection string support 
 
### Authentication 
 
- **PyJWT 2.8.0**: JSON Web Token generation and validation 
- **Authlib 1.3.0**: OAuth 2.0 client library for Google authentication 
- **Werkzeug 3.0.1**: Password hashing utilities 
 
### Utilities 
- **python-dotenv 1.0.0**: Environment variable management from .env files 
- **requests 2.31.0**: HTTP library for external API calls (Google OAuth user info) 
 
 ### Why These Technologies 
 Flask was chosen for its simplicity and flexibility, allowing rapid development without the overhead of larger frameworks. MongoDB provides schema flexibility that accommodates evolving data structures without migrations. The vanilla JavaScript approach keeps the frontend lightweight and avoids framework dependencies. Tailwind CSS enables rapid UI development with consistent styling. 
 

 ## Folder Structure 
 
. 
├── app/ # Main application package 
│ ├── __init__.py # Application factory, blueprint registration, dashboard route 
│ ├── config.py # Configuration class loading environment variables 
│ ├── models/ # Data models 
│ │ └── user_model.py # User document structure helpers 
│ ├── repositories/ # Database access layer 
│ │ ├── db.py # MongoDB connection management 
│ │ ├── client_repository.py # Client CRUD operations 
│ │ ├── project_repository.py # Project CRUD operations 
│ │ ├── invoice_repository.py # Invoice CRUD operations 
│ │ └── time_log_repository.py # Time log CRUD operations 
│ ├── services/ # Business logic layer 
│ │ ├── auth_service.py # User registration and authentication 
│ │ ├── oauth_service.py # Google OAuth user creation/lookup 
│ │ ├── client_service.py # Client business logic 
│ │ ├── project_service.py # Project business logic 
│ │ ├── invoice_service.py # Invoice calculation and generation 
│ │ ├── time_log_service.py # Timer start/stop logic 
│ │ └── search_service.py # Global search across entities 
│ ├── routes/ # HTTP request handlers 
│ │ ├── auth_routes.py # Authentication endpoints 
│ │ ├── client_routes.py # Client management endpoints 
│ │ ├── project_routes.py # Project management endpoints 
│ │ ├── invoice_routes.py # Invoice management endpoints 
│ │ ├── time_routes.py # Time log viewing endpoints 
│ │ └── search_routes.py # Global search endpoint 
│ ├── templates/ # Jinja2 HTML templates 
│ │ ├── base.html # Base template with navigation and AJAX handlers 
│ │ ├── base_auth.html # Base template for auth pages 
│ │ ├── dashboard.html # Dashboard with metrics 
│ │ ├── intro.html # Landing page 
│ │ ├── auth/ # Authentication templates 
│ │ ├── clients/ # Client templates (list, detail, edit, partial) 
│ │ ├── projects/ # Project templates (list, detail, edit, partial) 
│ │ ├── invoices/ # Invoice templates (list, detail, partial) 
│ │ ├── search/ # Search results templates 
│ │ └── time/ # Time log templates 
│ ├── utils/ # Utility modules 
│ │ ├── auth_decorators.py # @login_required decorator 
│ │ └── jwt_utils.py # JWT token creation and validation 
│ └── static/ # Static assets 
│ ├── css/ # Additional stylesheets 
│ └── js/ # Additional JavaScript files 
├── run.py # Application entry point 
├── requirements.txt # Python dependencies 
├── Procfile # Production server configuration 
├── setup_mongodb.py # Database setup script 
├── verify_connection.py # MongoDB connection verification 
└── .env # Environment variables (not in repo) 
 
 Key File Responsibilities 

 **app/__init__.py**: Creates the Flask application instance, registers all blueprints, initializes Google OAuth if configured, sets up ProxyFix middleware for production deployments, and defines the dashboard route with metric calculations. 

 **app/config.py**: Centralizes configuration by loading environment variables into a Config class. Handles MongoDB URI, JWT secrets, Google OAuth credentials, and Flask URL generation settings. 
 
 **app/repositories/db.py**: Manages MongoDB connection lifecycle. Implements singleton pattern for the client connection, handles both local and Atlas connections with appropriate SSL settings, and provides get_db() function for accessing the database instance. 
 
 **app/utils/auth_decorators.py**: Provides the @login_required decorator that validates JWT tokens from cookies, queries the database for user existence, and sets g.current_user for use in route handlers. 

 **app/utils/jwt_utils.py**: Handles JWT token creation with user ID and email payload, token validation and decoding, and error handling for expired or invalid tokens. 

 **run.py**: Entry point that imports the application factory, creates the app instance, and runs it on the configured port. In production, Gunicorn imports this module directly. 


 ## Setup Instructions 

 ### Prerequisites 
 - Python 3.8 or higher 
 - MongoDB instance (local or MongoDB Atlas) 
 - Git for version control 
 - Virtual environment tool (venv or virtualenv) 
 
 ### Building and Deployment 
 
The application is configured for deployment on Render (or similar platforms). No build step is required as Python is interpreted. 
 
1. Push code to your Git repository 
2. Connect repository to Render 
3. Set environment variables in Render dashboard 
4. Render will automatically: 
- Install dependencies from `requirements.txt` 
- Run the application using the `Procfile` command: `gunicorn run:app` 
- Listen on the PORT environment variable 
 
The `Procfile` specifies: 
``` 
web: gunicorn run:app 
``` 
 
This tells Render to use Gunicorn as the WSGI server, importing the `app` object from `run.py`. 
 
### Common Errors and Fixes 
 
**MongoDB Connection Error**: Verify `FCH_MONGO_URI` is correct. For Atlas, ensure your IP address is whitelisted in Network Access settings. Check that the database user has appropriate permissions. 
 
**JWT Token Errors**: Ensure `FCH_JWT_SECRET_KEY` is set and consistent. Clear browser cookies if experiencing authentication issues. 
 
**Google OAuth Redirect Mismatch**: Verify `FCH_SERVER_NAME` matches your deployment domain exactly. In Google Cloud Console, ensure redirect URIs include both `http://localhost:5000/auth/google/callback` (development) and your production URL. 
 
**Module Import Errors**: Ensure virtual environment is activated and all dependencies are installed. Check that you're running commands from the project root directory. 
 
**Port Already in Use**: Change the PORT in `.env` or stop the process using the port. On Unix systems, use `lsof -i :5000` to find the process. 
 
## Configuration 
 
### Config Class (app/config.py) 
 
The Config class loads all environment variables at application startup. It uses `python-dotenv` to read from `.env` files, falling back to environment variables if the file doesn't exist. This allows for different configurations between development and production without code changes. 
 
Configuration values are accessed throughout the application via `Config.MONGO_URI`, `Config.SECRET_KEY`, etc. The class provides default values for development but requires proper values in production. 
 
### Procfile 
 
The Procfile specifies how Render should run the application in production. The `web` process type runs Gunicorn, which is a production-grade WSGI server. Gunicorn handles multiple concurrent requests and is more suitable for production than Flask's development server. 
 
### requirements.txt 
 
Lists all Python package dependencies with specific versions. This ensures consistent environments across development and production. When deploying, the hosting platform installs these packages automatically. 