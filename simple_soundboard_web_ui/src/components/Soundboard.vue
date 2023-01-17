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
        <b-col><b-button size="sm" variant="danger" @click="stop_sounds()">Stop sounds</b-button></b-col>
      </b-row>
    </b-card>
    <p/>
    <b-card>
      <h3 v-if="current_folder == ''">
        Current Folder: root
      </h3>
      <h3 v-else>
        <b-button @click="folder_back()" variant="primary" style="float: left">Back</b-button> Current Folder: {{ current_folder }}
      </h3>
    </b-card>
    <p/>
    <draggable class="row row-cols-3" handle=".handle" v-model="folder_info.content">
      <b-col v-for="(file, i) in folder_info.content" :key="i">
        <div class="card" style="margin-bottom:10px">
          <div class="card-body action-bg">
            <div style="float: left;" class="handle"><b-icon icon="grip-horizontal" font-scale="1"></b-icon></div>
            <template v-if="file.is_folder">
              <div style="width: 100%;" @click="set_current_folder(file)">
                <template v-if="file.display_name.trim()">
                  {{ file.display_name }}<br/>
                </template>
                <template v-else>
                  {{ file.filename.split("/").at(-1) }}<br/>
                </template>
                <b-icon :icon="file.icon" font-scale="2.3"></b-icon>
              </div>
              <div style="float: right;" v-b-toggle="'collapse'+i">
                <span class="float-right when-opened">
                    <b-icon icon="caret-down-square-fill" />
                </span>
                <span class="float-right when-closed">
                    <b-icon icon="caret-down-square" />
                </span>
              </div>
              <div class="row">
                &nbsp;
              </div>
              <b-collapse :id="'collapse'+i">
                <div class="row">
                  <label class="col-md-3">Display Name</label>
                  <div class="col-md-9">
                    <b-form-input size="sm" v-model="file.display_name"></b-form-input>
                  </div>
                </div>
                <div class="row">
                  <label class="col-md-3">Icon</label>
                  <div class="col-md-9">
                    <b-form-input size="sm" v-model="file.icon"></b-form-input>
                  </div>
                </div>
                <br/>
                <div class="row">
                  <label class="col-md-3">Delete</label>
                  <div class="col-md-9">
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
                          Delete folder? All file inside will be deleted!</p>
                      </b-modal>
                  </div>
                </div>
              </b-collapse>
            </template>
            <template v-else>
              <div style="width: 100%;" class="btn-ripple" @click="playSound(file)">
                <b-icon v-if="file.is_music" icon="music-note" font-scale="1"></b-icon>
                <b-icon v-if="file.is_music" icon="music-note" font-scale="1"></b-icon>
                <b-icon v-if="file.is_music" icon="music-note" font-scale="1"></b-icon>
                <br/>
                <label>
                  <b-icon :icon="file.icon" font-scale="1"></b-icon>
                  <template v-if="file.display_name.trim()">
                    {{ file.display_name }}<br/>
                  </template>
                  <template v-else>
                    {{ file.filename.split("/").at(-1) }}<br/>
                  </template>
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
                  <label class="col-md-3">Display Name</label>
                  <div class="col-md-9">
                    <b-form-input size="sm" v-model="file.display_name"></b-form-input>
                  </div>
                </div>
                <div class="row">
                  <label class="col-md-3">Music?</label>
                  <div class="col-md-9">
                    <b-form-checkbox v-model="file.is_music"></b-form-checkbox>
                  </div>
                </div>
                <div class="row">
                  <label class="col-md-3">MQTT Topic</label>
                  <div class="col-md-9">
                    <b-form-input size="sm" v-model="file.mqtt_topic"></b-form-input>
                  </div>
                </div>
                <div class="row">
                  <label class="col-md-3">Icon</label>
                  <div class="col-md-9">
                    <b-form-input size="sm" v-model="file.icon"></b-form-input>
                  </div>
                </div>
                <!-- <div class="row">
                  <label class="col-md-3">Start Time</label>
                  <div class="col-md-9">
                    <b-form-input size="sm" v-model.number="file.start_time"></b-form-input>
                  </div>
                </div> -->
                <br/>
                <div class="row">
                  <label class="col-md-3">Delete</label>
                  <div class="col-md-9">
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
            </template>
          </div>
        </div>
      </b-col>
    </draggable>
    <b-form-file ref="fileInput" v-model="upload_file" style="display: none" plain @input="uploadConfig(upload_file)"></b-form-file>
    <b-row cols="3">
      <b-col class="ml-md-auto">
        <b-card>
          <b-row>
            <b-col>
              <b-button variant="primary" @click="triggerUpload()">Upload new sound</b-button>
            </b-col>
            <b-col>
              <b-button variant="primary" v-b-modal="'new_folder_modal'">Create new folder</b-button>
              <b-modal
                              id="new_folder_modal"
                              ref="modal"
                              title="Confirm action"
                              @ok="create_new_folder(new_folder_name)"
                              okVariant='primary'
                              okTitle='Yes'
                            >
                        <p class="my-4">
                          New folder name
                          <b-form-input size="sm" v-model="new_folder_name"></b-form-input></p>
                      </b-modal>
            </b-col>
          </b-row>
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
      upload_file: null,
      new_folder_name: ""
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
          return this.$store.getters["getCurrentFolder"]
      },
      set(value) {
          this.$store.commit('setCurrentFolder', value)
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
    set_current_folder(value) {
      this.current_folder = value.filename
      this.get_folder_info();
    },
    folder_back() {
      this.current_folder = this.current_folder.split("/").slice(0,-1).join("/");
      this.get_folder_info();
    },
    playSound(value) {
      console.log(value.filename);
      this.$store.dispatch('playSound', value)
    },
    get_folder_info() {
      this.$store.dispatch('getFolderInfo', this.current_folder)
    },
    create_new_folder(new_folder_name) {
      this.$store.dispatch('createNewFolder', this.current_folder + "/" + new_folder_name)
      .then(this.get_folder_info());
    },
    stop_sounds() {
      this.$store.dispatch('stopSounds')
    },
    stop_all() {
      this.$store.dispatch('stopAll')
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
      this.get_folder_info();
    },
    save_folder_info() {
      this.$store.dispatch('saveFolderInfo', {current_folder: this.current_folder, folder_info: this.folder_info})
      this.get_folder_info();
    },
    triggerUpload() {
      this.$refs.fileInput.$el.click()
    },
    uploadConfig() {
      var data = this.$refs.fileInput.files[0];
      var filename = this.$refs.fileInput.files[0].name;
      console.log(filename)
      this.$store.dispatch('uploadFile', {data: data, current_folder: this.current_folder, filename: filename})
      .then(this.get_folder_info());
    },
    delete_file(file) {
      this.$store.dispatch('delete_file', file)
      .then(this.get_folder_info());
    },
  },
  created() {
    this.get_folder_info();
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

div .row {
  padding-left: 10px !important;
  padding-right: 10px !important;
}
div .col {
  padding-left: 5px !important;
  padding-right: 5px !important;
}

.btn-ripple {
	display: inline-block;
	position: relative;
	overflow: hidden;
	transition: all ease-in-out .5s;
}

.btn-ripple::after {
	content: "";
	display: block;
	position: absolute;
	top: 0;
	left: 25%;
	height: 100%;
	width: 50%;
	background-color: rgb(16, 120, 255);
	border-radius: 50%;
	opacity: 0;
	pointer-events: none;
	transition: all ease-in-out 1s;
	transform: scale(5, 5);
}

.btn-ripple:active::after {
	padding: 0;
	margin: 0;
	opacity: .2;
	transition: 0s;
	transform: scale(0, 0);
}

</style>
