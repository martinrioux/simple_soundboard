<template>
  <div>
    <b-card>
      <b-row>
        <template v-if="folder_info_changed">
          <b-col ><b-button size="lg" variant="warning" @click="save_folder_info()">Save folder config</b-button></b-col>
        </template>
        <b-col ><b-button size="lg" variant="primary" @click="revert_folder_info()">Reload folder config</b-button></b-col>
        <b-col><b-button size="lg" variant="secondary" @click="fadeout_music()">Fadeout Music</b-button></b-col>
        <b-col><b-button size="lg" variant="danger" @click="stop_all_sounds()">Stop all sounds</b-button></b-col>
      </b-row>
    </b-card>
    <p/>
    <b-card>
      <h3>
        Current Folder: {{ current_folder == '' ? 'root' : current_folder}}
      </h3>
    </b-card>
    <p/>
    <draggable class="row row-cols-3" v-model="folder_info.content">
      <b-col v-for="file in folder_info.content" :key="file.filename">
        <div class="card" style="margin-bottom:10px">
          <div class="card-body action-bg">
            <div @click="playSound(file)" style="bg-color=black;">
              <label>
                <b-icon v-if="file.icon" :icon="file.icon" font-scale="1"></b-icon>
                <b-icon v-if="file.is_music" icon="music-note" font-scale="1"></b-icon>
                {{ file.filename }}
                <b-icon v-if="file.is_music" icon="music-note" font-scale="1"></b-icon>
                <b-icon v-if="file.is_music" :icon="file.icon" font-scale="1"></b-icon>
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
            <div class="col-md-2" v-b-toggle="'collapse'+file.filename">
                <span class="float-right when-opened">
                    <b-icon icon="caret-down-square-fill" />
                </span>
                <span class="float-right when-closed">
                    <b-icon icon="caret-down-square" />
                </span>
            </div>
            </div>
            <b-collapse :id="'collapse'+file.filename">
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
              <br/>
              <div class="row">
                <label class="col-md-6">Delete</label>
                <div class="col-md-6">
                  <b-button v-b-modal="'delete_modal'+file.filename" variant="danger" size="sm"><b-icon icon="trash"></b-icon></b-button>
                  <b-modal
                            :id="'delete_modal'+file.filename"
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

</style>
