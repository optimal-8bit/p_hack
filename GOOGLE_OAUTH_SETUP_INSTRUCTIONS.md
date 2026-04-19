# Google OAuth Setup Instructions

## The Error You're Seeing

The "Error 400: redirect_uri_mismatch" occurs because the redirect URI in your Google Cloud Console doesn't match your current domain. Here's how to fix it:

## Step 1: Access Google Cloud Console

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project (or create a new one if needed)
3. Navigate to "APIs & Services" > "Credentials"

## Step 2: Configure OAuth 2.0 Client

1. Find your OAuth 2.0 Client ID: `979659203690-hqcc5roaaf3kepil085k4ghq7e27h6av.apps.googleusercontent.com`
2. Click on it to edit
3. In the "Authorized JavaScript origins" section, add:
   - `http://localhost:3000` (for local development)
   - `http://localhost:5173` (for Vite dev server)
   - `https://yourdomain.com` (for production)
   - Any other domains where your app will run

4. In the "Authorized redirect URIs" section, add:
   - `http://localhost:3000` (for local development)
   - `http://localhost:5173` (for Vite dev server)  
   - `https://yourdomain.com` (for production)

## Step 3: Alternative Solution - Use Google Identity Services

I've created a new implementation using Google Identity Services which is more reliable and doesn't require redirect URI configuration. The new component `GoogleSignInButton` uses:

- Google Identity Services (GSI) instead of OAuth flow
- Proper JWT ID token handling
- No redirect URI requirements
- Better error handling

## Step 4: Test the New Implementation

1. The new `GoogleSignInButton` component is now integrated
2. It uses Google's official button styling
3. Handles JWT ID tokens properly
4. Should work without redirect URI issues

## Step 5: If You Still Get Errors

If you continue to see issues:

1. **Check your domain**: Make sure you're accessing the app from a domain listed in Google Cloud Console
2. **Clear browser cache**: Clear cookies and cache for Google accounts
3. **Try incognito mode**: Test in a private/incognito browser window
4. **Check console logs**: Look for detailed error messages in browser console

## Step 6: Production Deployment

When deploying to production:

1. Add your production domain to Google Cloud Console
2. Update the authorized origins and redirect URIs
3. Ensure HTTPS is enabled (required for production)
4. Test thoroughly before going live

## Current Configuration

**Client ID**: `979659203690-hqcc5roaaf3kepil085k4ghq7e27h6av.apps.googleusercontent.com`

**Domains to Add**:
- `http://localhost:3000`
- `http://localhost:5173` 
- `http://127.0.0.1:3000`
- `http://127.0.0.1:5173`
- Your production domain (with HTTPS)

## Troubleshooting

**Common Issues**:
1. **Wrong domain**: Using IP address instead of localhost
2. **Missing HTTPS**: Production requires HTTPS
3. **Cache issues**: Old tokens cached in browser
4. **Wrong port**: Using different port than configured

**Solutions**:
1. Always use `localhost` for local development
2. Use HTTPS for production
3. Clear browser data and try again
4. Match the exact port in Google Console

The new implementation should resolve the redirect URI mismatch error you're experiencing.