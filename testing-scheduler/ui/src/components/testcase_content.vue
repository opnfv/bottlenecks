<template>
  <div class="wrapper wrapper-content animated fadeIn">
    <div class="row" style="margin-bottom: 20px;">
      <div class="col-md-8">
        <ol class="breadcrumb" style="padding-left: 20px; font-size: 17px;">
          <li>
            <router-link to="/" >root</router-link>
          </li>
          <li>
            <router-link :to="{ path: '/stories', query: { name: suitename }}" >{{this.$route.query.suiteName}}</router-link>
          </li>
          <li>
            <router-link :to="{ path: '/content', query: { suiteName: suitename, caseName: casename } }"><b>{{this.$route.query.caseName}}</b></router-link>
          </li>
        </ol>
      </div>
    </div>


    <div id="p2_content1" style="" class="row">
      <div class="col-lg-12">
        <div class="ibox">
            <div class="ibox-title">
                <h5 style="font-size:26px;margin-top: -3px;">Test Case Content</h5>
                <div v-show="contentLoading || contentSaving" class="sk-spinner sk-spinner-circle" style="float: left;margin-left: 10px;">
                    <div class="sk-circle1 sk-circle"></div>
                    <div class="sk-circle2 sk-circle"></div>
                    <div class="sk-circle3 sk-circle"></div>
                    <div class="sk-circle4 sk-circle"></div>
                    <div class="sk-circle5 sk-circle"></div>
                    <div class="sk-circle6 sk-circle"></div>
                    <div class="sk-circle7 sk-circle"></div>
                    <div class="sk-circle8 sk-circle"></div>
                    <div class="sk-circle9 sk-circle"></div>
                    <div class="sk-circle10 sk-circle"></div>
                    <div class="sk-circle11 sk-circle"></div>
                    <div class="sk-circle12 sk-circle"></div>
                </div>
                <div class="ibox-tools">
                    <button class="btn btn-info btn-sm my-button-sm" type="button" v-on:click="runTestcase()">Run</button>
                    <button class="btn btn-success btn-sm my-button-sm" type="button" v-on:click="setEditable()">Edit</button>
                    <button v-show="isEditable" class="btn btn-warning btn-sm my-button-sm" v-on:click="saveTestcase()" type="button">Save</button>
                    <button v-show="isEditable" class="btn btn-danger btn-sm my-button-sm" v-on:click="cancelEdit()" type="button">Cancel</button>
                    <a class="collapse-link">
                        <i class="fa fa-chevron-up"></i>
                    </a>
                    <a class="fullscreen-link">
                        <i class="fa fa-expand"></i>
                    </a>
                </div>
            </div>
            <div class="ibox-content" style="max-height: 600px; overflow-y: auto; padding: 0; border: 1px solid #e7e7e7;">
                <div style='text-align:center;'>
                  <textarea v-show='!isEditable' v-model="content" id="tc_content" style="max-width:2400px; width: 100%;height: 100%;min-height: 500px;font-size:16px;border:none; vertical-align: middle; padding: 30px 0 0 40px;">
                  </textarea>
                </div><editor v-show='isEditable' v-bind:saveSignal='saveSignal' v-bind = 'editorContent' v-on:saveResponse='processSaveResponse'></editor>
            </div>
        </div>
      </div>
      
    </div>

    <hr />
    <div class="row">
      <div class="col-lg-12">
          <div class="ibox">
              <div class="ibox-title">
                  <h5 style="font-size:26px;margin-top: -3px;">Workflow</h5>
                  <div class="ibox-tools">
                      <a class="collapse-link">
                          <i class="fa fa-chevron-up"></i>
                      </a>
                      <a class="fullscreen-link">
                          <i class="fa fa-expand"></i>
                      </a>
                  </div>
              </div>
              <div class="ibox-content" style="padding-top: 60px;">
                  <wfresult v-bind:workflowId="workflowId" v-bind:wfloading='wfloading' v-bind:wfJson='wfJson'></wfresult>
              </div>
          </div>
      </div>

    </div>

  </div>
</template>
<script>
import {addClass, removeClass, isContainClass} from '../assets/js/my-util.js'
import editor from './editor/editor.vue'
import wfresult from './workflow_graph/wfresult.vue'
import toastr from '../assets/js/toastr.min.js'
  var content;
  var suitename;
function showMessage(type, title, msg){
  if(type == "success"){
    toastr.success(msg,title);
  }
  else if(type == "info") {
    toastr.info(msg, title);
  }
  else if(type == "error"){
    toastr.error(msg,title);
  }
  else {
    toastr.warning(msg, title);
  }
}
export default {
  name: 'testcase_content',
  data () {
    return {
      content,
      editorContent: {'stepList': [], 'mainOrdersList': [], 'subflowList': []},
      bakContent: '',
      isEditable: false,
      contentLoading: false,
      contentSaving: false,
      suitename:this.$route.query.suiteName,
      casename:this.$route.query.caseName,
      SERVER_ADDR: "http://localhost:5310/",
      workflowId: '',
      wfloading: false,
      wfJson: '',
      stories: [],
      services: [
        'greet',
        'yardstick',
        'logic'
      ],
      service_selected: '',
      selected: [],
      saveSignal: false
    }
  },
  created: function() {
      this.getTestcase();
  },
  computed: {
    selectAll: {
      get: function () {
        return this.stories ? this.selected.length == this.stories.length : false;
      },
      set: function (value) {
        var selected = [];

        if (value) {
          this.stories.forEach(function (story) {
            selected.push(story.id);
          });
        }
        this.selected = selected;
      }
    }
  },
  methods: {
    setEditable: function(){
      this.isEditable = true;
      this.bakContent = this.content;
    },
    cancelEdit: function(){
      this.content = this.bakContent;
      this.isEditable = false;
    },
    saveTestcase: function(){
      console.log("save");
      this.saveSignal = true;
      this.contentSaving = true;
    },
    runTestcase: function(){
      var self = this;
      $.ajax({
          url: this.global.SERVER_ADDR + "run-test/story",
          method: "POST",
          data: {
              "service": this.$route.query.suiteName,
              "stories": this.$route.query.caseName
          },
          beforeSend: function(XHR) {
              self.wfloading = true;
              showMessage("info", "run testcase", "start to run " + self.$route.query.caseName);
          },
          success: function(data) {
              console.log("ajax run test story!");
              self.wfloading = false;
              self.workflowId = data['result']['workflowId'];
              showMessage("success", "run testcase", " " + self.$route.query.caseName + " finished!");
              $.ajax({
                  url: self.global.SERVER_ADDR + "story-content",
                  method: "GET",
                  data: {
                      "service":  self.$route.query.suiteName,
                      "story": self.$route.query.caseName
                  },
                  success: function(data) {
                      if(data['code'] == 200) {
                          self.wfJson = data['result']['content'];
                      }
                  }
              });
          },
          error: function(err) {
              self.wfloading = false;
              showMessage("error", "run testcase", "server error!");
          }
      });
    },
    getTestcase: function(){
        var self = this;
        $.ajax({
          url: this.global.SERVER_ADDR + "testcase/content",
          method:"GET",
          data:{
            suiteName:  this.$route.query.suiteName,
            caseName: this.$route.query.caseName
          },
          beforeSend: function(XHR) {
              self.contentLoading = true;
          },
          success:function (data) {
            if(data['code'] == 200) {
              self.content = data['result']['content'];
              self.contentLoading = false;
              /*var eContent = data['result']['editorContent'];
              self.editorContent['stepList'] = eContent['stepList'];
              self.editorContent['mainOrdersList'] = eContent['mainOrdersList'];
              self.editorContent['subflowList'] = eContent['subflowList'];
              */
              self.editorContent = data['result']['editorContent'];
            }
            else {
              showMessage("failed", "content error", "fail to load testcase content!");
              self.contentLoading = false;
            }
          },
          error: function (error) {
            showMessage("failed", "content error", "fail to load testcase content!");
            self.contentLoading = false;
          }
        });
    },
    getOutput: function() {
        console.log("get output active!");
        var wfConfigDiv = document.getElementById("workflowId");
        var inputArr = wfDiv.getElementsByTagName("input");
        var idElem = inputArr[0];
        var workflowId = idElem.getAttribute("value");
        var url = this.global.WF_SERVER_ADDR + "workflow/" + workflowId + "?includeTasks=true";
        $.ajax({
            url: url,
            method: "GET",
            success: function(data) {
                console.log("get output:");
                console.log(data);
            }
        });
    },
    async processSaveResponse(result) {
      if(result == true) {
        // await this.sleep(5000);
        this.saveSignal = false;
        this.isEditable = false;
        this.contentSaving = false;
        showMessage("success", "operation ok", "save content success!");
        this.getTestcase();
      } else {
        // await this.sleep(5000);
        this.saveSignal = false;
        this.contentSaving = false;
        showMessage("error", "operation error", "failed to save content!");
      }
    },
    sleep: function(d) {  
        return new Promise((resolve) => setTimeout(resolve, d))  
    }
  },
  components: {
    editor,
    wfresult
  }
}
</script>
