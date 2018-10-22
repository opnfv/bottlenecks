<template>
  <div class="wrapper wrapper-content animated fadeIn">
    <div class="row" style="margin-bottom: 20px;">
      <div class="col-md-12">
        <ol class="breadcrumb" style="padding-left: 20px; font-size: 17px;">
          <li>
            <router-link to="/" >root</router-link>
          </li>
          <li>
            <router-link :to="{ path: '/testcase', query: { name: sname }}"><b>{{this.$route.query.name}}</b></router-link>
          </li>
        </ol>
      </div>
    </div>
    <div id="page-content" style="" class="row">
        <div class="col-lg-12">
            <div class="ibox">
                <div class="ibox-title">
                    <h5 style="font-size:26px;margin-top: -3px;">Test Case</h5>
                    <div class="ibox-tools">
                    <button class="btn btn-info btn-sm my-button-sm" type="button" v-on:click="runMultiTestcase()">Run</button>
                    <button class="btn btn-success btn-sm my-button-sm" type="button" v-on:click="create()">Create</button>
                    <button class="btn btn-danger btn-sm my-button-sm" v-on:click="deleteCases()" type="button">Delete</button>
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
                              <td class="checkbox1" style="width:20px"><input type="checkbox" v-model="selectAll"> All</td>
                              <td class="smallbox" style="with:250px;">TestCase Name</td>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="testcase in testcases">
                          <td><input class="checkbox1" style="width:20px" type="checkbox" v-model="selected" :value="testcase.testcase"> </td>
                          <td class="smallbox" style="with:250px;"><router-link :to="{ path: '/content', query: { suiteName: sname, caseName: testcase.testcase } }">{{testcase.testcase}}</router-link></td>
                        </tr>
                    </tbody>
                    <tfoot id="create-box" style="display: none">
                        <tr>
                            <td class="checkbox1" style="width:20px"><input type="checkbox"> </td>
                            <td class="smallbox" style="with:250px;"><input type="text" v-model="newCase" @keydown.enter="additem" ></td>
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
                            <tr v-for="testcase in runTestcases">
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
  name: 'testcase',
  data () {
    return {
      testcases: [],
      sname: this.$route.query.name,
      newCase:'',
      addstory:'',
      workflowId: '',
      wfloading: false,
      wfJson: '',
      selected: [],
      curRunningId: 0,
      runTestcases: [],
      wfComplete: false,
      runYet: false
    }
  },
  created: function() {
    var self = this;
    var msgTitle = "GET -- TESTCASES";
    var errorInfo = "Failed to get testcase list.";
    $.ajax({
      url: this.global.SERVER_ADDR + "testsuite/content",
      method:"GET",
      data:{
        suiteName:  this.$route.query.name
      },
      success:function (data) {
        if(data['code'] == 200) {
          self.testcases = data['result'];
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
        return this.testcases ? this.selected.length == this.testcases.length : false;
      },
      set: function (value) {
        var selected = [];
        if (value) {
          this.testcases.forEach(function (testcase) {
            selected.push(testcase.testcase);
          });
        }
        this.selected = selected;
      }
    }
  },
  methods:{
    create: function () {
      var cbox = document.getElementById("create-box");
      cbox.style.display = "table-footer-group";
    },
    additem: function () {
      var self = this;
      var msgTitle = "CREATE -- TESTCASE";
      const caseName = self.newCase.trim();
      if(caseName)
      {
        $.ajax({
          url: this.global.SERVER_ADDR + "testcase/new",
          method:"POST",
          data:{
            suiteName: self.sname,
            caseName: caseName
          },
          success:function (data) {
            if(data['code'] == 200){
              self.testcases.push({
                id: self.testcases.length + 1 ,
                testcase: caseName,
              });
              showMessage(data['code'], msgTitle, "Create <strong>" + caseName + "</strong> succesfully!");
            } else {
              showMessage(data['code'], msgTitle, "Failed to create <strong>" + caseName + "</strong>!", data['error']);
            }
          },
          error: function(obj, status, msg) {
            showMessage(status, msgTitle, "Failed to create <strong>" + caseName + "</strong>!", msg);
          }
        });
      }
      var cbox = document.getElementById("create-box");
      cbox.style.display = "none";
      this.newCase = '';
    },
    deleteCases:function () {
      var self = this;
      var msgTitle = "DELETE -- TESTCASE";
      var deleteArr = self.selected.slice(0);
      self.testcases = self.testcases.filter(item => {
          for(var i in deleteArr) {
            if(item.testcase == deleteArr[i]) {
              return false;
            }
          }
          return true;
      });
      self.selected = [];
      for(var i in deleteArr)
      {
        $.ajax({
          url: this.global.SERVER_ADDR + "testcase/delete",
          method: "POST",
          data: {
            suiteName: self.sname,
            caseName: deleteArr[i]
          },
          success: function(data) {
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
    runMultiTestcase: function() {
      var self = this;
      var msgTitle = "RUN -- TESTCASES";
      if(!self.runYet) {
        self.runYet = true;
      }
      self.runTestcases = [];
      if(self.selected.length == 0) {
        showMessage("warning", msgTitle, "please select one!");
        return;
      }
      for(var i=0; i < self.selected.length; i++) {
        var testcaseItem = {'id': i, 'testcase': '', 'status': "waiting"};
        testcaseItem['testcase'] = self.selected[i];
        self.runTestcases.push(testcaseItem);
      }
      self.curRunningId = 0;
      showMessage("info", msgTitle, "start to run <strong>testcases</strong>");
      self.runOneTestcase();
    },
    runOneTestcase: function() {
      var self = this;
      var msgTitle = "RUN -- TESTCASE";
      if (self.curRunningId == self.runTestcases.length) {
        self.curRunningId = 0;
        return;
      }
      self.wfComplete = false;
      var i = self.curRunningId;
      self.runTestcases[i]['status'] = "running";
      $.ajax({
          url: self.global.SERVER_ADDR + "execute/testcase",
          method: "POST",
          data: {
              "suiteName": self.sname,
              "caseName": self.runTestcases[self.curRunningId]['testcase']
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
                          "service":  self.sname,
                          "story": self.runTestcases[self.curRunningId]['testcase']
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
                self.runTestcases[i]['status'] = "failed";
                self.wfloading = false;
                showMessage(data['code'], msgTitle, "Failed to run <strong>" + self.runTestcases[i]['testcase'] + "</strong>", data['error']);
              }
          },
          error: function(obj, status, msg) {
            var i = self.curRunningId;
            self.runTestcases[i]['status'] = "failed";
            self.wfloading = false;
            showMessage(status, msgTitle, "Failed to run <strong>" + self.runTestcases[i]['testcase'] + "</strong>", msg);
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
      this.runOneTestcase();
    }
  },
  watch: {
    wfComplete: function(val) {
      if(val == false) return;
      this.wfloading = false;
      var i = this.curRunningId++;
      this.runTestcases[i]['status'] = "pass";
      this.runOneTestcase();
    }
  },
  components: {
    wfresult
  }
}
</script>
