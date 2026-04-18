import { createAsyncThunk, createSlice } from '@reduxjs/toolkit'

import { clearAccessToken, getAccessToken, setAccessToken } from '../../lib/authToken'
import { authService } from '../../services/authService'

export const registerUser = createAsyncThunk('auth/registerUser', async (payload) => {
  const result = await authService.register(payload)
  setAccessToken(result.access_token)
  return result
})

export const loginUser = createAsyncThunk('auth/loginUser', async (payload) => {
  const result = await authService.login(payload)
  setAccessToken(result.access_token)
  return result
})

export const loginWithGoogle = createAsyncThunk('auth/loginWithGoogle', async (credential) => {
  const result = await authService.loginWithGoogle(credential)
  setAccessToken(result.access_token)
  return result
})

export const fetchCurrentUser = createAsyncThunk('auth/fetchCurrentUser', async () => {
  return authService.me()
})

const initialState = {
  token: getAccessToken(),
  user: null,
  status: 'idle',
  error: null,
}

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    logout(state) {
      clearAccessToken()
      state.token = null
      state.user = null
      state.status = 'idle'
      state.error = null
    },
    clearAuthError(state) {
      state.error = null
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(registerUser.pending, (state) => {
        state.status = 'loading'
        state.error = null
      })
      .addCase(registerUser.fulfilled, (state, action) => {
        state.status = 'succeeded'
        state.token = action.payload.access_token
        state.user = action.payload.user
      })
      .addCase(registerUser.rejected, (state, action) => {
        state.status = 'failed'
        state.error = action.error.message || 'Registration failed'
      })
      .addCase(loginUser.pending, (state) => {
        state.status = 'loading'
        state.error = null
      })
      .addCase(loginUser.fulfilled, (state, action) => {
        state.status = 'succeeded'
        state.token = action.payload.access_token
        state.user = action.payload.user
      })
      .addCase(loginUser.rejected, (state, action) => {
        state.status = 'failed'
        state.error = action.error.message || 'Login failed'
      })
      .addCase(loginWithGoogle.pending, (state) => {
        state.status = 'loading'
        state.error = null
      })
      .addCase(loginWithGoogle.fulfilled, (state, action) => {
        state.status = 'succeeded'
        state.token = action.payload.access_token
        state.user = action.payload.user
      })
      .addCase(loginWithGoogle.rejected, (state, action) => {
        state.status = 'failed'
        state.error = action.error.message || 'Google login failed'
      })
      .addCase(fetchCurrentUser.fulfilled, (state, action) => {
        state.user = action.payload
      })
      .addCase(fetchCurrentUser.rejected, (state) => {
        clearAccessToken()
        state.token = null
        state.user = null
      })
  },
})

export const { logout, clearAuthError } = authSlice.actions

export default authSlice.reducer
