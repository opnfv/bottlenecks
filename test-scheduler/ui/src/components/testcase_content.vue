<template>
  <div class="wrapper wrapper-content animated fadeIn">
    <div class="row" style="margin-bottom: 20px;">
      <div class="col-md-12">
        <ol class="breadcrumb" style="padding-left: 20px; font-size: 17px;">
          <li>
            <router-link to="/" >root</router-link>
          </li>
          <li>
            <router-link :to="{ path: '/testcase', query: { name: suitename }}" >{{this.$route.query.suiteName}}</router-link>
          </li>
          <li>
            <router-link :to="{ path: '/content', query: { suiteName: suitename, caseName: casename } }"><b>{{this.$route.query.caseName}}</b></router-link>
          </li>
        </ol>
      </div>
    </div>
    <div id="page-content" class="row">
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
                  <textarea v-show='!isEditable' v-model="content" id="tc_content" style="white-space:nowrap; overflow:scroll;max-width:2400px; width: 100%;height: 100%;min-height: 500px;font-size:16px;border:none; vertical-align: middle; padding: 30px 0 20px 40px;">
                  </textarea>
                </div><editor v-show='isEditable' v-bind:saveSignal='saveSignal' v-bind = 'editorContent' v-on:saveResponse='processSaveResponse'></editor>
            </div>
        </div>
      </div>
    </div>
    <hr />
    <div class="row" v-show="runYet">
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
import editor from './editor/editor.vue'
import wfresult from './workflow_graph/wfresult.vue'
import showMessage from './message/showMessage.js'
export default {
    name: 'testcase_content',
    data () {
      return {
          content: '',
          editorContent: {'stepList': [], 'mainOrdersList': [], 'subflowList': []},
          bakContent: '',
          isEditable: false,
          contentLoading: false,
          contentSaving: false,
          suitename:this.$route.query.suiteName,
          casename:this.$route.query.caseName,
          workflowId: '',
          wfloading: false,
          wfJson: '',
          wfComplete: false,
          saveSignal: false,
          runYet: false,
      }
    },
    created: function() {
        this.getTestcase();
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
        var msgTitle = "RUN -- TESTCASE";
        if(!self.runYet) {
          self.runYet = true;
        }
        $.ajax({
            url: this.global.SERVER_ADDR + "execute/testcase",
            method: "POST",
            data: {
                "suiteName": this.$route.query.suiteName,
                "caseName": this.$route.query.caseName
            },
            beforeSend: function(XHR) {
                self.wfloading = true;
                showMessage("info", msgTitle, "start to run <strong>" + self.$route.query.caseName + "</strong>");
            },
            success: function(data) {
                if(data['code'] == 200) {
                    self.workflowId = data['result']['workflowId'];
                    showMessage(data['code'], msgTitle, "<strong>" + self.$route.query.caseName + "</strong> finished!");
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
                            } else {
                              showMessage(data['code'], msgTitle, "workflow.json get failed!");
                            }
                        },
                        error: function(obj, status, msg) {
                          showMessage(status, msgTitle, msg);
                        }
                    });
                } else {
                  self.wfloading = false;
                  showMessage(data['code'], msgTitle, "Failed to run <strong>" + self.$route.query.caseName + "</strong>", data['error']);
                }
            },
            error: function(obj, status, msg) {
                self.wfloading = false;
                showMessage(status, msgTitle, "Failed to run <strong>" + self.$route.query.caseName + "</strong>", msg);
            }
        });
      },
      getTestcase: function(){
          var self = this;
          var msgTitle = "GET -- TESTCASE";
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
                self.editorContent = data['result']['editorContent'];
              }
              else {
                showMessage("error", msgTitle, "fail to load testcase content!", data['error']);
                self.contentLoading = false;
              }
            },
            error: function (obj, status, msg) {
              showMessage(status, msgTitle, "fail to load testcase content!", msg);
              self.contentLoading = false;
            }
          });
      },
      async processSaveResponse(result) {
          if(result == true) {
            this.saveSignal = false;
            this.isEditable = false;
            this.contentSaving = false;
            this.getTestcase();
          } else {
            this.saveSignal = false;
            this.contentSaving = false;
          }
      }
    },
    components: {
      editor,
      wfresult
    }
}
</script>
