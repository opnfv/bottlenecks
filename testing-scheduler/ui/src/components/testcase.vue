<template>
  <div class="wrapper wrapper-content">
    <div class="row" style="margin-bottom: 20px;">
      <div class="col-md-8">
        <ol class="breadcrumb" style="padding-left: 20px; font-size: 17px;">
          <li>
            <router-link to="/" >root</router-link>
          </li>
          <li>
            <router-link :to="{ path: '/stories', query: { name: sname }}"><b>{{this.$route.query.name}}</b></router-link>
          </li>
        </ol>
      </div>
    </div>
    <div id="p2_content1" style="" class="row">
        <div class="col-lg-8">
            <div class="ibox">
                <div class="ibox-title">
                    <h5 style="font-size:26px;margin-top: -3px;">Test Case</h5>
                    <div class="ibox-tools">
                    <button class="btn btn-info btn-sm my-button-sm" type="button" v-on:click="runTestcases()">Run</button>
                    <button class="btn btn-success btn-sm my-button-sm" type="button" v-on:click="create()">Create</button>
                    <button class="btn btn-danger btn-sm my-button-sm" v-on:click="deleteyaml()" type="button">Delete</button>
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
                              <td class="smallbox" style="with:250px;">TestSuite Name</td>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="yaml in yamls">
                          <td><input class="checkbox1" style="width:20px" type="checkbox" v-model="selected" :value="yaml.testcase"> </td>
                          <td class="smallbox" style="with:250px;"><router-link :to="{ path: '/content', query: { suiteName: sname, caseName: yaml.testcase } }">{{yaml.testcase}}</router-link></td>
                        </tr>
                    </tbody>
                    <tfoot id="create-box" style="display: none">
                        <tr>
                            <td class="checkbox1" style="width:20px"><input type="checkbox"> </td>
                            <td class="smallbox" style="with:250px;"><input type="text" v-model="newstory" @keydown.enter="additem" ></td>
                        </tr>
                    </tfoot>
                  </table>                             
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
                <div id="executing" class="col-md-2" style="height:600px; margin-right: 200px;">
                    <table class="table" style="margin-top: 30px;">
                      <tr style="border-top-width: 1px;border-top-style: solid;">
                        <td style="padding-right: 8px">1</td>
                        <td style="padding-right: 8px">opnfv_bottleneck_ts001.yaml</td>
                        <td style="padding-right: 8px"><p class="text-success">pass</p></td>
                      </tr>
                      <tr style="border-top-width: 1px;border-top-style: solid;">
                        <td>2</td>
                        <td>opnfv_bottleneck_ts002.yaml</td>
                        <td><p class="text-success">pass</p></td>
                      </tr >
                      <tr style="border-top-width: 1px;border-top-style: solid;">
                        <td>3</td>
                        <td>opnfv_bottleneck_ts003.yaml</td>
                        <td><p class="text-success">pass</p></td>
                      </tr>
                      <tr style="border-top-width: 1px;border-top-style: solid;">
                        <td>4</td>
                        <td>opnfv_bottleneck_ts004.yaml</td>
                        <td><p class="text-warning">running</p></td>
                      </tr>
                    </table>
                </div> 

                  <wfresult v-bind:workflowId="workflowId" v-bind:wfloading='wfloading' v-bind:wfJson='wfJson'></wfresult>
              </div>
          </div>
      </div>

    </div>


  </div>
</template>
<script>
import {addClass, removeClass, isContainClass} from '../assets/js/my-util.js'
import wfresult from './workflow_graph/wfresult.vue'
var yamls;
var sname;
export default {
  name: 'testcase',
  data () {
    return {
      yamls,
      sname: this.$route.query.name,
      newstory:'',
      addstory:'',
      workflowId: '',
      wfloading: false,
      wfJson: '',
      selected: []
    }
  },
  created: function() {
    var self = this;
    $.ajax({
      url: this.global.SERVER_ADDR + "testsuite/content",
      method:"GET",
      data:{
        suiteName:  this.$route.query.name
      },
      success:function (data) {
        if(data['code'] == 200) {
          self.yamls = data['result'];
        }
      }
    });
  },
  computed: {
    selectAll: {
      get: function () {
        return this.yamls ? this.selected.length == this.yamls.length : false;
      },
      set: function (value) {
        var selected = [];

        if (value) {
          this.yamls.forEach(function (yaml) {
            selected.push(yaml.testcase);
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
      const  storytext = self.newstory.trim()
      if(storytext )
      {
        $.ajax({
          url: this.global.SERVER_ADDR + "testcase/new",
          method:"GET",
          data:{
            suiteName: self.sname,
            caseName: storytext
          },
          success:function (data) {
            if(data['code'] == 200){
              self.yamls.push({
                id: self.yamls.length + 1 ,
                testcase: storytext,
              })
            }
          }
        })

      }
      var cbox = document.getElementById("create-box");
      cbox.style.display = "none";
      this.newstory = '';
    },
    deleteyaml:function () {
      var self = this;
      for(var n in self.selected)
      {
        $.ajax({
          url: this.global.SERVER_ADDR + "testcase/delete",
          method:"GET",
          data:{
            suiteName: self.sname,
            caseName: self.selected[n]
          },
          success:function (data) {
            if(data['code'] == 200)
            {
              self.yamls = self.yamls.filter(yaml => {
                return yaml.testcase !== self.selected[n]

              })
            }

          }
        })

      }

    },
    addyaml:function () {
      const  yamltext = this.addstory.trim()
      if(yamltext)
      {
        this.yamls.push({
          id: this.yamls.length + 1 ,
          storyname: yamltext,
        })
      }
      var cbox = document.getElementById("add-box");
      cbox.style.display = "none";
      this.addstory = '';

    },
    runTestcases: function() {
      var self = this;
      $.ajax({
          url: this.global.SERVER_ADDR + "run-test/story",
          method: "POST",
          data: {
              "service": this.$route.query.name,
              "stories": this.selected[0]
          },
          beforeSend: function(XHR) {
              self.wfloading = true;
          },
          success: function(data) {
              console.log("ajax run test story!");
              self.wfloading = false;
              self.workflowId = data['result']['workflowId'];
          }
      });

      $.ajax({
          url: this.global.SERVER_ADDR + "story-content",
          method: "GET",
          data: {
              "service":  this.$route.query.name,
              "story": this.selected[0]
          },
          success: function(data) {
              if(data['code'] == 200) {
                  self.wfJson = data['result']['content'];
              }
          }
      });    
    }
  },
  components: {
    wfresult
  }
}
</script>
