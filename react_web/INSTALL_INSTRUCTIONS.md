# Frontend Installation Instructions

## Step 1: Clean Previous Installation

```bash
# Remove node_modules and lock file
rm -rf node_modules package-lock.json

# On Windows PowerShell:
Remove-Item -Recurse -Force node_modules, package-lock.json
```

## Step 2: Install Dependencies

```bash
npm install
```

## Step 3: Create Environment File

```bash
# Create .env file
echo "VITE_API_BASE_URL=http://localhost:8000/api/v1" > .env

# On Windows PowerShell:
"VITE_API_BASE_URL=http://localhost:8000/api/v1" | Out-File -FilePath .env -Encoding utf8
```

## Step 4: Start Development Server

```bash
npm run dev
```

## If Installation Still Fails

Try with legacy peer deps flag:

```bash
npm install --legacy-peer-deps
```

## Verify Installation

After successful installation, you should see:
- `node_modules/` folder created
- `package-lock.json` file created
- No error messages

Then start the dev server:
```bash
npm run dev
```

The app should be available at: http://localhost:5173
