#!/usr/bin/env python3
"""
OAuth Diagnostic Script
Run this to test your Google OAuth configuration
"""

from app import create_app

app = create_app()

with app.app_context():
    from flask import url_for
    from app.config import Config
    
    print("=" * 60)
    print("Google OAuth Configuration Test")
    print("=" * 60)
    print()
    
    # Check credentials
    print("1. Credentials Check:")
    print("-" * 60)
    print(f"   Client ID: {'✅ Set' if Config.GOOGLE_CLIENT_ID else '❌ Missing'}")
    if Config.GOOGLE_CLIENT_ID:
        print(f"   Client ID length: {len(Config.GOOGLE_CLIENT_ID)}")
        print(f"   Client ID ends with: {Config.GOOGLE_CLIENT_ID[-30:]}")
    print(f"   Client Secret: {'✅ Set' if Config.GOOGLE_CLIENT_SECRET else '❌ Missing'}")
    if Config.GOOGLE_CLIENT_SECRET:
        print(f"   Client Secret length: {len(Config.GOOGLE_CLIENT_SECRET)}")
    print()
    
    # Check OAuth client
    print("2. OAuth Client Initialization:")
    print("-" * 60)
    google_oauth = app.config.get('GOOGLE_OAUTH')
    if google_oauth:
        print("   ✅ OAuth client is initialized")
    else:
        print("   ❌ OAuth client is NOT initialized")
        print("   This means credentials are missing or invalid")
    print()
    
    # Check redirect URI
    print("3. Redirect URI Check:")
    print("-" * 60)
    try:
        redirect_uri = url_for('auth.google_callback', _external=True)
        print(f"   ✅ Redirect URI: {redirect_uri}")
        print()
        print("   ⚠️  IMPORTANT: This URI must match EXACTLY in Google Console:")
        print(f"      {redirect_uri}")
        print()
        print("   Go to: https://console.cloud.google.com/")
        print("   → APIs & Services → Credentials")
        print("   → Click on your OAuth 2.0 Client ID")
        print("   → Check 'Authorized redirect URIs'")
        print("   → Make sure this exact URI is listed:")
        print(f"      {redirect_uri}")
    except Exception as e:
        print(f"   ❌ Error generating redirect URI: {e}")
    print()
    
    # Check login URL
    print("4. Login URL Check:")
    print("-" * 60)
    try:
        login_url = url_for('auth.google_login', _external=True)
        print(f"   ✅ Google login URL: {login_url}")
        print()
        print("   To test, visit this URL in your browser:")
        print(f"   {login_url}")
    except Exception as e:
        print(f"   ❌ Error generating login URL: {e}")
    print()
    
    print("=" * 60)
    print("Next Steps:")
    print("=" * 60)
    print()
    print("1. Verify the redirect URI above matches Google Console")
    print("2. Make sure you're added as a test user (if in testing mode)")
    print("3. Or publish your app (if you want any user to sign in)")
    print("4. Check that JavaScript origin is set: http://localhost:5000")
    print("5. Try the login URL above")
    print()

