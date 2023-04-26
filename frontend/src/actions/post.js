import axios from "axios";
import { setAlert } from "./alert";
import {
  GET_POSTS,
  GET_POST,
  POST_ERROR,
  UPDATE_LIKES,
  DELETE_POST,
  ADD_POST,
  ADD_COMMENT,
  REMOVE_COMMENT
} from './types'

export const getPosts = () => async dispatch => {
  try {
    const response = await axios.get('/api/v1/posts')

    dispatch({ type: GET_POSTS, payload: response.data })
  } catch (e){
    dispatch({
      type: POST_ERROR,
      payload: { msg: e.response.statusText, status: e.response.status }
    })
  }
}


export const getPost = postId => async dispatch => {
  try{
    const response = await axios.get(`/api/v1/posts/${postId}`)

    dispatch({ type: GET_POST, payload: response.data })
  } catch (e) {
    dispatch({
      type: POST_ERROR,
      payload: { msg: e.response.statusText, status: e.response.status }
    })
  }
}


export const toggleLike = postId => async dispatch => {
  try {
    const response = await axios.post(`/api/v1/posts/${postId}/like`)

    dispatch({ type: UPDATE_LIKES, payload: response.data })
  } catch (e) {
    dispatch({
      type: POST_ERROR,
      payload: {msg: e.response.statusText, status: e.response.status }
    })
  }
}


export const deletePost = postId => async dispatch => {
  try {
    await axios.delete(`api/v1/posts/${postId}`)

    dispatch({ type: DELETE_POST, payload: postId })
    dispatch(setAlert('Post Removed', 'success'))
  } catch (e) {
    dispatch({
      type: POST_ERROR,
      payload: { msg: e.response.statusText, status: e.response.status }
    })
  }
}


export const addPost = formData => async dispatch => {
  const config = {
    headers: { 'Content-Type': 'application/json' }
  }
  try {
    const response = await axios.post('api/v1/posts', formData, config)

    dispatch({ type: ADD_POST, payload: response.data })
    dispatch(setAlert('Post Added', 'success'))
  } catch (e) {
    dispatch({
      type: POST_ERROR,
      payload: { msg: e.response.statusText, status: e.response.status }
    })
  }
}

export const addComment = (postId, formData) => async dispatch => {
  const config = {
    headers: { "Content-Type": "application/json" }
  };
  try {
    const res = await axios.post(
      `/api/posts/${postId}/comments`,
      formData,
      config
    );

    dispatch({ type: ADD_COMMENT, payload: res.data });
    dispatch(setAlert("Comment Added", "success"));
  } catch (err) {
    dispatch({
      type: POST_ERROR,
      payload: { msg: err.response.statusText, status: err.response.status }
    });
  }
};


export const deleteComment = (postId, commentId) => async dispatch => {
  try {
    await axios.delete(`/api/posts/comments/${commentId}`);

    dispatch({ type: REMOVE_COMMENT, payload: commentId });
    dispatch(setAlert("Comment Removed", "success"));
  } catch (err) {
    dispatch({
      type: POST_ERROR,
      payload: { msg: err.response.statusText, status: err.response.status }
    });
  }
};