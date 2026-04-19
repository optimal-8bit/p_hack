import { useEffect, useRef } from 'react'
import { useDispatch } from 'react-redux'
import { useNavigate } from 'react-router-dom'
import { loginWithGoogle } from '../../features/auth/authSlice'

const GoogleSignInButton = ({ text = "Continue with Google", onSuccess, onError }) => {
  const dispatch = useDispatch()
  const navigate = useNavigate()
  const buttonRef = useRef(null)
  const googleRef = useRef(null)

  useEffect(() => {
    const initializeGoogleSignIn = () => {
      if (window.google && window.google.accounts) {
        window.google.accounts.id.initialize({
          client_id: "979659203690-hqcc5roaaf3kepil085k4ghq7e27h6av.apps.googleusercontent.com",
          callback: handleCredentialResponse,
          auto_select: false,
          cancel_on_tap_outside: true,
        })

        // Render the button
        if (buttonRef.current) {
          window.google.accounts.id.renderButton(buttonRef.current, {
            theme: "outline",
            size: "large",
            width: "100%",
            text: "continue_with",
            shape: "rectangular",
          })
        }

        googleRef.current = window.google
      }
    }

    const handleCredentialResponse = async (response) => {
      try {
        console.log('🔐 Google credential response:', response)
        
        // The response.credential contains the JWT ID token
        const result = await dispatch(loginWithGoogle(response.credential)).unwrap()
        
        console.log('✅ Google login successful:', result)
        
        if (onSuccess) {
          onSuccess(result)
        } else {
          // Default navigation based on user role
          if (result.user.role === 'doctor') {
            navigate('/doctor-dashboard')
          } else {
            navigate('/chat')
          }
        }
      } catch (error) {
        console.error('❌ Google login error:', error)
        if (onError) {
          onError(error)
        }
      }
    }

    // Load Google Identity Services script if not already loaded
    if (!window.google) {
      const script = document.createElement('script')
      script.src = 'https://accounts.google.com/gsi/client'
      script.async = true
      script.defer = true
      script.onload = initializeGoogleSignIn
      document.head.appendChild(script)
    } else {
      initializeGoogleSignIn()
    }

    // Cleanup function
    return () => {
      if (googleRef.current && googleRef.current.accounts) {
        // Clean up Google Sign-In
        try {
          googleRef.current.accounts.id.cancel()
        } catch (e) {
          // Ignore cleanup errors
        }
      }
    }
  }, [dispatch, navigate, onSuccess, onError])

  return (
    <div style={{ width: '100%' }}>
      <div ref={buttonRef} style={{ width: '100%' }}></div>
    </div>
  )
}

export default GoogleSignInButton