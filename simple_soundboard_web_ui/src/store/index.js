import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios';

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    config: {},
    current_folder: "",
    folder_info: {},
    initial_folder_info: {info: ""}
  },
  mutations: {
    setConfig(state, data) {
      state.config = data;
    },
    setFolderInfo(state, data) {
      state.initial_folder_info.info = JSON.stringify(data);
      state.folder_info = data;
    }
  },
  actions: {
    getConfig({ commit }) {
      return axios.get('/api/get_config')
        .then( function(result) {
          commit('setConfig', result.data);
          return result.data
      })
        .catch(console.error);
    },
    getFolderInfo({ commit }, current_folder) {
      return axios.post('/api/get_folder_info', {current_folder: current_folder})
        .then( function(result) {
          commit('setFolderInfo', result.data);
          return result.data
      })
        .catch(console.error);
    },
    playSound({}, value) {
      return axios.post('/api/play_sound', {file: value})
        .then( function(result) {
          return result.data
      })
        .catch(console.error);
    },
    stopAllSounds({}) {
      return axios.get('/api/stop_all_sounds')
        .then( function(result) {
          return result.data
      })
        .catch(console.error);
    },
    fadeoutMusic({}) {
      return axios.get('/api/fadeout_music')
        .then( function(result) {
          return result.data
      })
        .catch(console.error);
    },
    saveFolderInfo({}, info) {
      return axios.post('/api/save_folder_info', info)
        .then( function(result) {
          return result.data
      })
        .catch(console.error);
    },
    delete_file({}, value) {
      return axios.post('/api/delete_file', {file: value})
        .then(function(result) {
          return result.data
      })
        .catch(console.error);
    },
    uploadFile({}, data) {
      return axios.post('/api/upload_file', data.data, {headers: {'current_folder': data.current_folder, filename: data.filename}})
        .then( function(result) {
          return result.data
      })
        .catch(console.error);
    },
  },
  getters: {
    getConfig(state) {
      return state.config
    },
    getFolderInfo(state) {
      return state.folder_info
    },
    getInitialFolderInfo(state) {
      return state.initial_folder_info.info
    }
  },
  modules: {
  }
})
