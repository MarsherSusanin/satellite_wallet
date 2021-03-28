import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

const API = 'http://35.184.30.28/api/1.0/'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    allert: {
      isActive: false,
      type: null,
      title: null,
      text: null
    },
    isLoading: false,
    user: null,
    auth: null,
    mnemonic: null,
    wallets: []
  },
  mutations: {
    showAllert (state, payload) { state.allert = { isActive: true, ...payload } },
    closeAllert (state) { state.allert = { isActive: false } },
    loaderOn (state) { state.isLoading = true },
    loaderOff (state) { state.isLoading = false },
    setUser (state, user) { state.user = user },
    setMnemonic (state, mnemonic) { state.mnemonic = mnemonic },
    setAuth (state, { login, password }) { state.auth = { login, password } },
    setWallets (state, wallets) { state.wallets = wallets }
  },
  actions: {
    send ({ commit }, options) {
      commit('loaderOn')
      return axios(options)
        .then(response => response.data)
        .then((payload) => {
          commit('loaderOff')
          return payload
        })
        .catch((err) => {
          commit('loaderOff')
          commit('showAllert', { type: 'error', title: 'error', text: err })
        })
    },
    registration ({ commit, dispatch }, data) {
      commit('setAuth', data)

      return dispatch('send', {
        method: 'post',
        url: `${API}newauth/`,
        data
      })
        /* eslint-disable camelcase */
        .then(({ user_id, session_id }) => {
          this.commit('setUser', { user_id, session_id })
        })
    },
    login ({ commit, dispatch }, data) {
      commit('setAuth', data)

      return dispatch('send', {
        method: 'post',
        url: `${API}auth/`,
        data
      })
        /* eslint-disable camelcase */
        .then(({ user_id, session_id }) => {
          this.commit('setUser', { user_id, session_id })
        })
    },
    getSeed ({ state, commit }) {
      return axios({
        method: 'post',
        url: `${API}genmnemonic/`,
        data: state.user
      })
        .then(response => response.data)
        .then((payload) => {
          commit('setMnemonic', payload.mnemonic)
          return payload
        })
        .catch((err) => {
          commit('showAllert', { type: 'error', title: 'error', text: err })
        })
    },
    createWallets ({ state, dispatch }) {
      return Promise.all([
        axios({
          method: 'post',
          url: `${API}genwallet/`,
          data: {
            user_id: state.user.user_id,
            session_id: state.user.session_id,
            coin_type: 'Atom',
            mnemonic: state.mnemonic
          }
        }),
        axios({
          method: 'post',
          url: `${API}genwallet/`,
          data: {
            user_id: state.user.user_id,
            session_id: state.user.session_id,
            coin_type: 'Kava',
            mnemonic: state.mnemonic
          }
        })
      ])
        .then((responseArr) => {
          console.log(responseArr)
          return responseArr.map(response => {
            console.log(response)
            if (response.data.address) {
              console.log(response.data.address)
              this.dispatch('saveWallet', response.data)
              return response.address
            }
          })
        })
    },
    saveWallet ({ commit }, { wallet_name, address }) {
      const wallets = JSON.parse(window.localStorage.getItem('wallets')) || []
      wallets.push({ wallet_name, address })
      window.localStorage.setItem('wallets', JSON.stringify(wallets))
      commit('setWallets', wallets)
    },
    loadWallets ({ commit }) {
      commit('setWallets', JSON.parse(window.localStorage.getItem('wallets')))
    },
    saveSeed ({ commit }, seed) {
      window.localStorage.setItem('mnemonic', seed)
      commit('setMnemonic', seed)
    },
    loadSeed ({ commit }) {
      commit('setMnemonic', window.localStorage.getItem('mnemonic'))
    }
  },
  modules: {
  }
})
