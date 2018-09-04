<template>
<!-- step -->
<div class="row">
    <div class="col-md-6 col-sm-12">
        <div class="ibox float-e-margins">
            <div class="ibox-title">
                <h5 class="text-success">Step</h5>
                <div class="ibox-tools" style="height: 25px;">
                    <button class="btn btn-success " type="button" id="new-step">&nbsp;&nbsp;<span class="bold">New Step</span></button>
                        <a class="collapse-link" >
                            <i class="fa fa-chevron-up" v-on:click.stop='collapseBox'></i>
                        </a>
                </div>
            </div>
            <div class="ibox-content" style="border: 1px solid #cec8c8">
                <form class="form-horizontal">
                    <div class="row">
                        <div class="form-group">
                            <label class="col-md-2 control-label">Name:</label>
                            <div class="col-md-5"><input type="text" class="form-control" id="name"></div>
                        </div>
                        <div class="form-group">
                            <label class="col-md-2 control-label">Service:</label>
                            <div class="col-md-4">
                                <select class="form-control" id="service">
                                    <option></option>
                                    <option v-for='service in dataService' v-bind:value='service'>{{service}}</option>
                                </select>
                            </div>
                        </div>
                        <div class="form-group">
                            <label class="col-md-2 control-label">Action:</label>
                            <div class="col-md-4">
                                <select class="form-control" id="action">
                                    <option></option>
                                    <option v-for='action in dataAction' v-bind:value='action.name'>{{action.name}}</option>
                                </select>
                            </div>
                        </div>
                    </div>
                    <div class="row" id="parameter">
                        <div class="form-group" v-for='(param, index) in dataParam'>
                            <label class="col-md-2 control-label" v-bind:title="param.description">{{ param.name }}
                            </label>
                            <div class="col-md-5">
                                <input type="text" class="form-control"  v-bind:placeholder="param.description" v-bind:id="'par'+index">
                            </div>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>
    <div class="col-md-6 col-sm-12">
        <div class="ibox float-e-margins">
            <div class="ibox-title">
                <h5 class="text-success">StepList</h5>
                <div class="ibox-tools">
                        <a class="collapse-link">
                            <i class="fa fa-chevron-up" v-on:click.stop='collapseBox'></i>
                        </a>
                </div>
            </div>
            <div class="ibox-content" id="step-list" style="border: 1px solid #cec8c8">
                <div v-for='(step, index) in stepList' class='ibox'>
                    <div class="ibox-title step">
                        <h5>Step{{index + 1}} &nbsp;&nbsp; {{step.name}} </h5>
                        <div class="ibox-tools">
                            <a class="collapse-link">
                                <i class="fa fa-chevron-up" v-on:click.stop='collapseBox'></i>
                            </a>
                            <a class="close-link" v-on:click='removeStep(index)'>
                                <i class="fa fa-times"></i>
                            </a>
                        </div>
                    </div>
                    <div class="ibox-content">
                        <div class="row">
                            <label class="control-label"><span style='padding-right: 20px;'>Service:</span> {{ step.service }}</label>
                        </div>
                        <div class="row">
                          <label class="control-label"><span style='padding-right: 20px;'>Action:</span> {{ step.action }}</label>
                        </div>
                           <div class="param row">
                          <label class="control-label">
                              <span style='padding-right: 20px;'>Parameter:</span>
                              <span v-for='param in step.params'>{{param.key}} = {{param.value}} ;&nbsp;&nbsp;&nbsp;</span>
                          </label>
                        </div>
                       </div>
                </div>
            </div>
        </div>
    </div>
</div>
</template>
<script>
export default {
    name: 'step',
    props: ['stepList'],
    data: function() {
        return {
            dataService: [],
            dataAction: [],
            dataParam: []
        }
    },
    mounted: function() {
        this.getServiceList();
        var self = this;
        $("#service").change(function(){
            self.selectService();
        });
        $("#action").change(function(){
            self.selectAction();
        });
        $('#new-step').click(function(){
            self.newStep();
        });
    },
    methods: {
        getServiceList: function(){
            console.log("get serviceList!");
            var self = this;
            $.ajax({
                url: this.global.SERVER_ADDR + "service/list",
                method: "GET",
                async:false,
                success: function(data){
                    console.log("ajax success!");
                    if(data['code'] == 200){
                        self.dataService = [];
                        self.dataService = data['result'];
                    }
                }
            });
        },
        getServiceContent: function(name){
            var self = this;
            $.ajax({
                url: this.global.SERVER_ADDR + "service/content",
                method: "GET",
                async:false,
                data: {
                    "serviceName": name
                },
                success: function(data){
                    if(data['code'] == 200){
                        self.dataAction = [];
                        self.dataAction = data['result']['actions'];
                    }
                }
            });
        },
        getParams: function(name){
            for(var i in this.dataAction){
                if(this.dataAction[i].name == name){
                    this.dataParam = [];
                    this.dataParam = this.dataAction[i].params;
                    break;
                }
            }
        },
        selectService: function(event){
            var selectedName = $("#service").val();
            this.getServiceContent(selectedName);
        },
        selectAction: function(event){
            var selectedName = $("#action").val();
            if(selectedName=="") {
                this.dataParam = [];
                return;
            }
            this.getParams(selectedName);
            if(this.dataParam==undefined) this.dataParam = [];
        },
        newStep: function(){
            var ser = $("#service").val();
            var act = $("#action").val();
            var na = $("#name").val();
            if(ser==""||act==""||na==""){
                alert('Not completed!');
                return;
            }
            var parCount = this.dataParam.length;
            var par = [];
            for(var i=0; i<parCount; ++i){
                var temp = $('#par'+i).val();
                if(temp==""){
                    alert('Not completed!');
                    return;
                }
                var name = this.dataParam[i].name;
                par.push({key: name, value: temp});
            }
            this.stepList.push({name: na, service: ser, action: act, params: par});
            $("#name").val("");
            $("#service").val("");
            this.dataAction = [];
            this.dataParam = [];
        },
        removeStep: function(index) {
            this.stepList.splice(index, 1);
        },
        collapseBox: function(event) {
            console.log("collapse");
            var ele = event.target;
            console.log(event);
            console.log(ele);
            var ibox = $(ele).closest('div.ibox');
            var content = ibox.children('.ibox-content');
            content.slideToggle(200);
            $(ele).toggleClass('fa-chevron-up').toggleClass('fa-chevron-down');
        }
    },
    watch: {
        stepList: function() {
            this.$emit('stepList', this.stepList);
        }
    }
}
</script>
