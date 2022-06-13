import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    token: localStorage.getItem('magnetdb_session_token'),
    user: null,
  },
  getters: {
    isLogged(state) {
      return !!state.token
    },
  },
  mutations: {
    setToken(state, token) {
      state.token = token

      if (token) {
        localStorage.setItem('magnetdb_session_token', token)
      } else {
        localStorage.removeItem('magnetdb_session_token')
        state.user = null
      }
    },
    setUser(state, user) {
      state.user = user
    },
  },
})

export default store
