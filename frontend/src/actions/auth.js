import axios from 'axios'
import { setAlert } from './alert'
import {
  REGISTER_SUCCESS,
  REGISTER_FAIL,
  USER_LOADED,
  AUTH_ERROR,
  LOGIN_SUCCESS,
  LOGIN_FAIL,
  LOGOUT,
  CLEAR_PROFILE,
} from './types'
import setAuthToken from '../utils/setAuthToken'


export const loadUser = () => async dispatch => {
  if (localStorage.token){
    setAuthToken(localStorage.token)
  }
  try {
    const response = await axios.get('api/v1/auth')

    dispatch({ type: USER_LOADED, payload: response.data })
  } catch(e) {
    dispatch({ type: AUTH_ERROR })
  }
}


export const register = ({ name, email, password }) => async dispatch => {
  const config = {
    headers: {'Content-Type': 'application/json'}
  }

  const body = JSON.stringify({ name, email, password })

  try { 
    const response = await axios.post('api/v1/users', body, config)

    dispatch({
      type: REGISTER_SUCCESS,
      payload: response.data.token
    })

    dispatch(loadUser())
  } catch(e){
    const errors = e.response.data

    if (errors['name']){
      errors['name'].forEach(msg =>
        dispatch(setAlert(`Name: ${msg}`, 'danger')) 
      )
    }

    if (errors['email']){
      errors['email'].forEach(msg =>
        dispatch(setAlert(`Email: ${msg}`, 'danger')) 
      )
    }

    if (errors["password"]) {
      errors["password"].forEach(msg =>
        dispatch(setAlert(`Password: ${msg}`, "danger"))
      );
    }

    dispatch({
      type: REGISTER_FAIL
    })
  }
}


export const login = ({email, password}) => async dispatch => {
  const config = {
    headers: { 'Content-Type': 'application/json' }
  }
  const body = JSON.stringify({ email, password })

  try{
    const response = await axios.post('api/v1/auth', body, config)

    dispatch({
      type: LOGIN_SUCCESS,
      payload: response.data.token
    })

    dispatch(loadUser())
  } catch(e){
    const error = e.response.data.error

    dispatch(setAlert(error, 'danger'))

    dispatch({
      type: LOGIN_FAIL
    })
  }
}


export const logout = () => dispatch => {
  dispatch({ type: LOGOUT })
  dispatch({ type: CLEAR_PROFILE })
}
