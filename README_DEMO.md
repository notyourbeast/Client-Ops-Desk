# Demo Mode Setup

This application can run in demo mode without MongoDB for quick demonstrations.

## Quick Start

1. **Enable demo mode:**
   ```bash
   export FCH_USE_MOCK_DB=true
   ```

2. **Run the application:**
   ```bash
   python run.py
   ```

   Or use the demo setup script:
   ```bash
   python demo_setup.py
   ```

## Demo Credentials

- **Email:** demo@example.com
- **Password:** demo

## What's Included

The demo mode includes:
- 1 demo user account
- 1 sample client (Acme Corp)
- 1 sample project (Website Redesign)
- 1 sample time log entry
- 1 sample invoice

## Environment Variables

You can set these in your `.env` file or as environment variables:

- `FCH_USE_MOCK_DB=true` - Enables mock database mode
- `FCH_SECRET_KEY` - Flask secret key (optional, defaults to 'dev-secret')
- `FCH_JWT_SECRET_KEY` - JWT secret key (optional, defaults to 'dev-jwt-secret')

## Notes

- All data is stored in memory and will be lost when the server restarts
- The mock database mimics MongoDB's interface, so no code changes are needed
- Perfect for demos, testing, or development without MongoDB setup

