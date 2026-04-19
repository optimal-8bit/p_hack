import { GoogleOAuthProvider } from '@react-oauth/google'
import './App.css'
import AppRouter from './routes/AppRouter'

const GOOGLE_CLIENT_ID = "979659203690-hqcc5roaaf3kepil085k4ghq7e27h6av.apps.googleusercontent.com"

function App() {
  return (
    <GoogleOAuthProvider 
      clientId={GOOGLE_CLIENT_ID}
      onScriptLoadError={() => console.error('Google OAuth script failed to load')}
      onScriptLoadSuccess={() => console.log('Google OAuth script loaded successfully')}
    >
      <AppRouter />
    </GoogleOAuthProvider>
  )
}

export default App
