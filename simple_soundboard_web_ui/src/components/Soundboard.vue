<template>
  <div>
    <b-card>
      <b-row>
        <template v-if="folder_info_changed">
          <b-col ><b-button size="sm" variant="warning" @click="save_folder_info()">Save folder config</b-button></b-col>
        </template>
        <b-col ><b-button size="sm" variant="primary" @click="revert_folder_info()">Reload folder config</b-button></b-col>
        <b-col><b-button size="sm" variant="secondary" @click="fadeout_music()">Fadeout Music</b-button></b-col>
        <b-col><b-button size="sm" variant="warning" @click="pause_music()">Pause music</b-button><b-button size="sm" variant="primary" @click="resume_music()">Resume music</b-button></b-col>
        <b-col><b-button size="sm" variant="danger" @click="stop_all_sounds()">Stop all sounds</b-button></b-col>
      </b-row>
    </b-card>
    <p/>
    <b-card>
      <h3>
        Current Folder: {{ current_folder == '' ? 'root' : current_folder}}
      </h3>
    </b-card>
    <p/>
    <draggable class="row row-cols-3" handle=".handle" v-model="folder_info.content">
      <b-col v-for="(file, i) in folder_info.content" :key="i">
        <div class="card" style="margin-bottom:10px">
          <div class="card-body action-bg">
            <div style="float: left;" class="handle"><b-icon icon="grip-horizontal" font-scale="1"></b-icon></div>
            <div @click="playSound(file)" style="bg-color=black;">
              <label>
                <b-icon :icon="file.icon" font-scale="1"></b-icon>
                <b-icon v-if="file.is_music" icon="music-note" font-scale="1"></b-icon>
                {{ file.filename }}
                <b-icon v-if="file.is_music" icon="music-note" font-scale="1"></b-icon>
                <b-icon :icon="file.icon" font-scale="1"></b-icon>
              </label>
            </div>
            <div class="row">
            <div class="col-md-2">
              <template v-if="file.is_music">
                <b-form-checkbox v-model="file.loop_playback"> <b-icon icon="arrow-repeat" font-scale="1"></b-icon></b-form-checkbox>
              </template>
            </div>
            <div class="col-md-8">
              <b-form-input v-model.number="file.volume" type="range" min="0" max="1" step="0.05"></b-form-input>
            </div>
            <div class="col-md-2" v-b-toggle="'collapse'+i">
                <span class="float-right when-opened">
                    <b-icon icon="caret-down-square-fill" />
                </span>
                <span class="float-right when-closed">
                    <b-icon icon="caret-down-square" />
                </span>
            </div>
            </div>
            <b-collapse :id="'collapse'+i">
              <div class="row">
                <label class="col-md-6">Music?</label>
                <div class="col-md-6">
                  <b-form-checkbox v-model="file.is_music"></b-form-checkbox>
                </div>
              </div>
              <div class="row">
                <label class="col-md-6">MQTT Topic</label>
                <div class="col-md-6">
                  <b-form-input size="sm" v-model="file.mqtt_topic"></b-form-input>
                </div>
              </div>
              <div class="row">
                <label class="col-md-6">Icon</label>
                <div class="col-md-6">
                  <b-form-input size="sm" v-model="file.icon"></b-form-input>
                </div>
              </div>
              <div class="row">
                <label class="col-md-6">Start Time</label>
                <div class="col-md-6">
                  <b-form-input size="sm" v-model.number="file.start_time"></b-form-input>
                </div>
              </div>
              <div class="row">
                <label class="col-md-6">Stop Time</label>
                <div class="col-md-6">
                  <b-form-input size="sm" v-model.number="file.stop_time"></b-form-input>
                </div>
              </div>
              <br/>
              <div class="row">
                <label class="col-md-6">Delete</label>
                <div class="col-md-6">
                  <b-button v-b-modal="'delete_modal'+i" variant="danger" size="sm"><b-icon icon="trash"></b-icon></b-button>
                  <b-modal
                            :id="'delete_modal'+i"
                            ref="modal"
                            title="Confirm action"
                            @ok="delete_file(file)"
                            okVariant='danger'
                            okTitle='Yes'
                          >
                      <p class="my-4">
                        Delete file?</p>
                    </b-modal>
                </div>
              </div>
            </b-collapse>
          </div>
        </div>
      </b-col>
    </draggable>
    <b-form-file ref="fileInput" v-model="upload_file" style="display: none" plain @input="uploadConfig(upload_file)"></b-form-file>
    <b-row cols="3">
      <b-col class="ml-md-auto">
        <b-card>
          <b-button variant="primary" @click="triggerUpload()">Upload new sound</b-button>
        </b-card>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import draggable from 'vuedraggable'

export default {
  components: {
      draggable,
  },
  name: 'Soundboard',
  data: function() {
    return {
      upload_file: null
    }
  },
  props: {
    msg: String
  },
  computed: {
    folder_info: {
      get() {
          return this.$store.getters["getFolderInfo"]
      },
      set(value) {
          this.$store.commit('setFolderInfo', value)
      }
    },
    current_folder: {
      get() {
          return this.$store.state.current_folder
      }
    },
    folder_info_changed: {
      get() {
        var changed = JSON.stringify(this.folder_info) != this.$store.getters["getInitialFolderInfo"]
        return changed
      }
    }
  },
  methods: {
    playSound(value) {
      console.log(value.filename);
      this.$store.dispatch('playSound', value)
    },
    get_folder_info(value) {
      this.$store.dispatch('getFolderInfo', value)
    },
    stop_all_sounds() {
      this.$store.dispatch('stopAllSounds')
    },
    fadeout_music() {
      this.$store.dispatch('fadeoutMusic')
    },
    pause_music() {
      this.$store.dispatch('pauseMusic')
    },
    resume_music() {
      this.$store.dispatch('resumeMusic')
    },
    revert_folder_info() {
      this.get_folder_info(this.current_folder);
    },
    save_folder_info() {
      this.$store.dispatch('saveFolderInfo', {current_folder: this.current_folder, folder_info: this.folder_info})
      this.get_folder_info(this.current_folder);
    },
    triggerUpload() {
      this.$refs.fileInput.$el.click()
    },
    uploadConfig() {
      var data = this.$refs.fileInput.files[0];
      var filename = this.$refs.fileInput.files[0].name;
      console.log(filename)
      this.$store.dispatch('uploadFile', {data: data, current_folder: this.current_folder, filename: filename})
      .then(this.get_folder_info(this.current_folder));
    },
    delete_file(file) {
      this.$store.dispatch('delete_file', file)
      .then(this.get_folder_info(this.current_folder));
    },
  },
  created() {
    this.get_folder_info(this.current_folder);
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.collapsed > .when-opened,
:not(.collapsed) > .when-closed {
    display: none;
}


.card {
  color: rgba(0, 0, 0, 1);
  background-color: rgba(255, 255, 255, 0.95) !important;
  margin-left: 0px !important;
  margin-right: 0px !important;
  padding-left: 3px !important;
  padding-right: 3px !important;
  padding-top: 3px !important;
  padding-bottom: 3px !important;
}
.card-body {
  margin-left: 0px !important;
  margin-right: 0px !important;
  padding-left: 3px !important;
  padding-right: 3px !important;
  padding-top: 3px !important;
  padding-bottom: 3px !important;
}

</style>
