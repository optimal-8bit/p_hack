# Fix ffmpeg PATH on Windows

## Quick Fix (Temporary - for current session only)

In your PowerShell terminal, run:

```powershell
# Replace with your actual ffmpeg path
$env:PATH += ";C:\ffmpeg\bin"

# Verify it works
ffmpeg -version
```

## Permanent Fix (Recommended)

### Option 1: Using PowerShell (Run as Administrator)

```powershell
# Replace C:\ffmpeg\bin with your actual path
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\ffmpeg\bin", "User")

# Restart PowerShell, then verify
ffmpeg -version
```

### Option 2: Using Windows Settings (GUI)

1. Press `Win + X` and select "System"
2. Click "Advanced system settings" on the right
3. Click "Environment Variables" button
4. Under "User variables", select "Path" and click "Edit"
5. Click "New" and add your ffmpeg bin path (e.g., `C:\ffmpeg\bin`)
6. Click "OK" on all dialogs
7. **Restart PowerShell** (important!)
8. Verify: `ffmpeg -version`

## Common ffmpeg Locations

- `C:\ffmpeg\bin`
- `C:\Program Files\ffmpeg\bin`
- `C:\Users\YourName\ffmpeg\bin`

Find your ffmpeg.exe location and add that folder to PATH.

## After Adding to PATH

1. **Close and reopen PowerShell** (important!)
2. Test: `ffmpeg -version`
3. Run verification: `python test_voice_imports.py`
4. Start server: `cd backend && python main.py`
