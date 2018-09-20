<template>
  <div class="wrapper wrapper-content animated fadeIn">
    <div class="row" style="margin-bottom: 20px;">
      <div class="col-md-12">
        <ol class="breadcrumb" style="padding-left: 20px; font-size: 17px;">
          <li>
            <router-link to="/" >root</router-link>
          </li>
        </ol>
      </div>
    </div>
    <div id="page-content" class="row">
      <div class="col-lg-12">
        <div class="ibox">
            <div class="ibox-title">
                <h5 style="font-size:26px;margin-top: -3px;">Test Suite</h5>
                <div class="ibox-tools">
                    <button class="btn btn-info btn-sm my-button-sm" type="button" v-on:click="runTestsuites()">Run</button>
                    <button class="btn btn-success btn-sm my-button-sm" type="button" v-on:click="createSuite()">Create</button>
                    <button class="btn btn-danger btn-sm my-button-sm" v-on:click="deleteSuites()" type="button">Delete</button>
                    <a class="collapse-link">
                        <i class="fa fa-chevron-up"></i>
                    </a>
                    <a class="fullscreen-link">
                        <i class="fa fa-expand"></i>
                    </a>
                </div>
            </div>
            <div class="ibox-content" style="text-align:center;">
              <table class="my-table table table-bordered" cellspacing="0" cellpadding="0" style="text-align: center;">
                <thead>
                  <tr>
                    <td style="width:20px"><input type="checkbox" v-model="selectAll"> All</td>
                    <td class="smallbox" style="with:250px;">TestSuite Name</td>
                  </tr>
                </thead>
                <tbody>
                    <tr v-for="testsuite in testsuites">
                      <td><input style="width:20px" type="checkbox" v-model="selected" :value="testsuite.testsuite"> </td>
                      <td class="smallbox" style="with:250px;"><router-link :to="{ path: '/testcase', query: { name: testsuite.testsuite }}" >{{testsuite.testsuite}}</router-link></td>
                    </tr>
                </tbody>
                <tfoot id="create-box" style="display: none">
                    <tr>
                      <td style="width:20px"><input type="checkbox"> </td>
                      <td class="smallbox" style="with:250px;"><input type="text" v-model="newSuite" @keydown.enter="addItem" ></td>
                    </tr>
                </tfoot>
              </table>
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
              <div class="ibox-content" style="padding-top: 30px;">
                <div id="executing" class="row" style="padding: 0 30px 60px;">
                  <div class="col-md-offset-2 col-md-8">
                      <div class="table-responsive">
                        <table class="table text-center" style="margin-top: 30px;">
                          <thead>
                            <tr>
                              <th class="text-center">#</th>
                              <th class="text-center">testcase</th>
                              <th class="text-center">status</th>
                              <th class="text-center">operation</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr v-for="testcase in casesInSuite">
                              <td>{{ testcase.id }}</td>
                              <td>{{ testcase.testcase }}</td>
                              <td><span class="badge" v-bind:class="'badge-' + statusClass(testcase.status)">{{ testcase.status }}</span></td>
                              <td>
                              <div style="display: inline-block;min-width: 130px;">
                                <button class="btn btn-primary btn-outline btn-xs fadeIn" v-on:click="runTestcase()" v-show="testcase.status == 'failed'">rerun</button>
                                <button class="btn btn-primary btn-outline btn-xs fadeIn" v-on:click="runNextCase($event.target)" v-show="testcase.status == 'failed'">run next one</button>
                              </div>
                              </td>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                  </div>
                </div>
                <hr class="hr-line-solid">
                <div class="row" style="margin-top: 60px;">
                  <wfresult v-bind:workflowId="workflowId" v-bind:wfloading='wfloading' v-bind:wfJson='wfJson' v-on:wfComplete="wfComplete = $event"></wfresult>
                </div>
              </div>
          </div>
      </div>
    </div>
  </div>
</template>
<script>
import wfresult from './workflow_graph/wfresult.vue'
import showMessage from './message/showMessage.js'
export default {
  name: 'testsuite',
  data () {
    return {
      newSuite : '',
      testsuites : '',
      service_selected : '',
      workflowId: '',
      wfloading: false,
      wfJson: '',
      selected: [],
      casesInSuite: [],
      running: {
        suiteName: "",
        caseName: ""
      },
      curRunningId: 0,
      wfComplete: false,
      runYet: false
    }
  },
  created: function() {
    var self = this;
    var msgTitle = "GET -- TESTSUITES";
    var errorInfo = "Failed to get testsuite list.";
    $.ajax({
      url: this.global.SERVER_ADDR + "testsuite/list",
      method:"GET",
      data:{},
      success:function (data) {
        if(data['code'] == 200) {
          self.testsuites = data['result'];
        } else {
          showMessage(data['code'], msgTitle, errorInfo, data['error']);
        }
      },
      error: function(obj, status, msg) {
        showMessage(status, msgTitle, errorInfo, msg);
      }
    });
  },
  computed: {
    selectAll: {
      get: function () {
        return this.testsuites ? this.selected.length == this.testsuites.length : false;
      },
      set: function (value) {
        var selected = [];
        if (value) {
          this.testsuites.forEach(function (story) {
            selected.push(story.testsuite);
          });
        }
        this.selected = selected;
      }
    }
},
  methods:{
    createSuite: function () {
      var cbox = document.getElementById("create-box");
      cbox.style.display = "table-footer-group";
    },
    addItem: function () {
      var self = this;
      const suiteName = self.newSuite.trim();
      if(suiteName)
      {
        var msgTitle = "CREATE -- TESTSUITE";
        $.ajax({
          url: this.global.SERVER_ADDR + "testsuite/new",
          method:"POST",
          data:{
            suiteName:suiteName
          },
          success:function(data){
            if(data['code'] == 200){
              self.testsuites.push({
                id: self.testsuites.length + 1 ,
                testsuite: suiteName,
              });
              showMessage(data['code'], msgTitle, "Create <strong>" + suiteName + "</strong> succesfully!");
            } else {
              showMessage(data['code'], msgTitle, "Failed to create <strong>" + suiteName + "</strong>!", data['error']);
            }
          },
          error: function(obj, status, msg) {
            showMessage(status, msgTitle, "Failed to create <strong>" + suiteName + "</strong>!", msg);
          }
        })
      }
      var cbox = document.getElementById("create-box");
      cbox.style.display = "none";
      this.newSuite = '';
    },
    deleteSuites:function () {
      var self = this;
      var msgTitle = "DELETE -- TESTSUITE";
      var deleteArr = self.selected.slice(0);
      self.testsuites = self.testsuites.filter(item => {
          for(var i in deleteArr) {
            if(item.testsuite == deleteArr[i]) {
              return false;
            }
          }
          return true;
      });
      self.selected = [];
      for(var i in deleteArr)
      {
        $.ajax({
          url: this.global.SERVER_ADDR + "testsuite/delete",
          method:"POST",
          data:{
            suiteName: deleteArr[i]
          },
          success:function (data) {
            if(data['code'] == 200){
              showMessage(data['code'], msgTitle, "Delete <strong>" + deleteArr[i] + "</strong> succesfully!");
            } else {
              showMessage(data['code'], msgTitle, "Failed to delete <strong>" + deleteArr[i] + "</strong>!", data['error']);
            }
          },
          error: function(obj, status, msg) {
            showMessage(status, msgTitle, "Failed to delete <strong>" + deleteArr[i] + "</strong>!", msg);
          }
        });
      }
    },
    runTestsuites: function() {
      var self = this;
      var msgTitle = "RUN -- TESTSUITE";
      if(!self.runYet) {
        self.runYet = true;
      }
      if(self.selected.length == 0) {
        showMessage("warning", msgTitle, "please select one!");
        return;
      } else if(self.selected.length != 1) {
        showMessage("warning", msgTitle, "sorry, one suite at a time!");
        return;
      }
      self.running.suiteName = self.selected[0];
      $.ajax({
        url: this.global.SERVER_ADDR + "testsuite/content",
        method: "GET",
        data: {
          "suiteName": self.running.suiteName
        },
        success: function(data) {
          if (data['code'] == 200) {
            var caseList = data['result'];
            if(caseList.length == 0) {
              showMessage("info", msgTitle, "<strong>" + self.running.suiteName + "</strong> is empty!");
              return;
            }
            for(var i=0; i < caseList.length; i++) {
              caseList[i]['status'] = "waiting";
            }
            self.casesInSuite = caseList;
            showMessage(data['code'], msgTitle, "Start to run <strong>" + self.running.suiteName + "</strong>");
            self.runTestcase();
          } else {
            showMessage(data['code'], msgTitle, "Failed to run <strong>" + self.running.suiteName + "</strong>", data['error']);
          }
        },
        error: function(obj, status, msg) {
          showMessage(status, msgTitle, "Failed to run <strong>" + self.running.suiteName + "</strong>", msg);
        }
      });
    },
    runTestcase: function() {
        var self = this;
        var msgTitle = "RUN -- TESTCASE";
        if (self.curRunningId == self.casesInSuite.length) {
          self.curRunningId = 0;
          return;
        }
        self.wfComplete = false;
        var i = self.curRunningId;
        self.casesInSuite[i]['status'] = "running";
        self.running.caseName = self.casesInSuite[i]['testcase'];
        $.ajax({
          url: self.global.SERVER_ADDR + "execute/testcase",
          method: "POST",
          data: {
              "suiteName": self.running.suiteName,
              "caseName": self.running.caseName
          },
          beforeSend: function(XHR) {
              self.wfloading = true;
          },
          success: function(data) {
              if(data['code'] == 200) {
                self.workflowId = data['result']['workflowId'];
                $.ajax({
                    url: self.global.SERVER_ADDR + "story-content",
                    method: "GET",
                    data: {
                        "service":  self.running.suiteName,
                        "story": self.running.caseName
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
                var i = self.curRunningId;
                self.casesInSuite[i]['status'] = "failed";
                self.wfloading = false;
                showMessage(data['code'], msgTitle, "Failed to run <strong>" + self.running.caseName + "</strong>", data['error']);
              }
          },
          error: function(obj, status, msg) {
            var i = self.curRunningId;
            self.casesInSuite[i]['status'] = "failed";
            self.wfloading = false;
            showMessage(status, msgTitle, "Failed to run <strong>" + self.running.caseName + "</strong>", msg);
          }
        });
    },
    statusClass: function(status) {
      if(status == "waiting") {
        return "success";
      }
      if(status == "running") {
        return "warning";
      }
      if(status == "pass") {
        return "primary";
      }
      if(status == "failed") {
        return "danger";
      }
    },
    runNextCase: function(obj) {
      $(obj).parent().css({"display": "none"});
      var i = this.curRunningId++;
      this.runTestcase();
    }
  },
  watch: {
    wfComplete: function(val) {
      if(val == false) return;
      this.wfloading = false;
      var i = this.curRunningId++;
      this.casesInSuite[i]['status'] = "pass";
      // run the next testcase.
      this.runTestcase();
    }
  },
  components: {
    wfresult
  }
}
</script>
