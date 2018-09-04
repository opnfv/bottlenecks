<template>
<div class="row" style="border: 1px solid #cec8c8">
    <div class="col-md-12" style="padding: 10px 0 5px;">
        <div class="form-group">
            <label class="col-md-2 control-label" style="font-size: 22px;">flowName</label>
            <div class="col-md-6">
                <input v-if="flowName != 'main'" type="text" class="form-control" v-model="flowName" v-on:input='$emit("editFlowName", $event.target.value)' placeholder="please input flow name." />
                <p style="font-size: 22px;" v-else>{{flowName}}</p>
            </div>
        </div>
    </div>
    <div class="col-md-12">
        <div class="ibox">
            <div class="ibox-title">
                <h5 class="text-success">Order</h5>
                <div class="ibox-tools">
                    <a class="collapse-link">
                        <i class="fa fa-chevron-up" v-on:click.stop='collapseBox'></i>
                    </a>
                </div>
            </div>
            <div class="ibox-content">
                <div class="row">
                    <button class="btn btn-success" type="button" id="new-order" v-on:click='addOrder'>&nbsp;&nbsp;<span class="bold">ADD ORDER</span></button>
                    <div class="col-md-3">
                       <span class="select-box" >
                        <select id="orderSelect" class="select form-control" v-model='orderSelected' >
                            <option value="1">Normal</option>
                            <option value="2">Switch</option>
                            <option value="3">Parallel</option>
                        </select>
                        </span>
                    </div>
                    <br>
                    <!-- Normal -->
                    <div id="normal-panel" v-show='orderSelected == 1'>
                        <div class="col-lg-11" id="normalform">
                            <br>
                            <div>
                                <div class="ibox border-ibox">
                                    <div class="ibox-title">
                                        <h5>Normal</h5>
                                        <div class="ibox-tools">
                                            <a class="collapse-link" >
                                                <i class="fa fa-chevron-up" v-on:click.stop='collapseBox'></i>
                                            </a>
                                        </div>
                                    </div>
                                    <div class="ibox-content">
                                       <!-- <div class="form-group">
                                          <div class="col-lg-6 row"><label>name</label><input id="NName" type="name" placeholder="name" class="form-control"></div>
                                       </div> -->
                                       <div class="form-group">
                                            <label class='headmsg control-label'>Step</label>
                                            <div class='col-md-4'>
                                                <select class="chooseStep form-control" id="NStep" v-model='normalStep'>
                                                        <option></option>
                                                        <option v-for='stepRef in stepsRefs' v-bind:value='stepRef'>{{ stepRef }}</option>
                                                </select>
                                            </div>
                                       </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <!-- Switch -->
                    <div id="switch-panel" v-show='orderSelected == 2'>
                        <br>
                        <div class="row">
                            <div class="col-lg-11">
                                <div class="ibox border-ibox float-e-margins">
                                    <div class="ibox-title">
                                        <h5>Switch</h5>
                                        <div class="ibox-tools">
                                            <button class="btn btn-success " type="button" id="new-case" v-on:click='addNewCase'>&nbsp;&nbsp;<span class="bold">New Case</span></button>
                                            <a class="collapse-link" >
                                                <i class="fa fa-chevron-up" v-on:click.stop='collapseBox'></i>
                                            </a>
                                        </div>
                                    </div>
                                    <div class="ibox-content">
                                        <div class="row">
                                            <div class="row">
                                                <div class="form-group">
                                                    <label class="headmsg control-label">Value:</label>
                                                    <div class="col-md-5"><input type="text" class="case form-control" v-model='switchValue'></div>
                                                </div>
                                            </div>
                                            <div class="row">
                                                <label class="headmsg control-label">Cases:</label>
                                                <div class='col-md-12 row'>
                                                    <div class='col-md-offset-1' v-for='switchCase in switchCases' style='border-left-style: solid; border-left-color: gray; margin-bottom: 30px;'>
                                                        <div class="row">
                                                            <div class="form-group">
                                                                <label class="headmsg control-label">CaseValue:</label>
                                                                <div class="col-md-5"><input type="text" class="case form-control" v-model='switchCase.value'></div>
                                                            </div>
                                                        </div>
                                                        <div class="row">
                                                            <label class="headmsg control-label">Case:</label>
                                                            <div class="col-md-3">
                                                                <select class="myselect chooseStep form-control" v-model='switchCase.orderType'>
                                                                    <option></option>
                                                                    <option v-for='orderType in ["step", "flow"]' v-bind:value='orderType'>{{ orderType }}</option>
                                                                </select>
                                                            </div>
                                                            <div class="col-md-4">
                                                                <select class="myselect chooseStep form-control" v-model='switchCase.orderValue'>
                                                                    <option></option>
                                                                    <option v-if='switchCase.orderType == "step"' v-for='stepRef in stepsRefs' v-bind:value='stepRef'>{{ stepRef }}</option>
                                                                    <option v-if='switchCase.orderType == "flow"' v-for='flowRef in filtedFlowsRefs' v-bind:value='flowRef'>{{ flowRef }}</option>
                                                                </select>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <!-- Parallel -->
                    <div id="parallel-panel" v-show='orderSelected == 3'>
                        <br>
                        <div class="row">
                            <div class="col-lg-11">
                                <div class="ibox border-ibox float-e-margins">
                                    <div class="ibox-title">
                                        <h5>Parallel</h5>
                                        <div class="ibox-tools">
                                            <button class="btn btn-success " type="button" id="para-step" v-on:click='addNewBranch'>&nbsp;&nbsp;<span class="bold"><i class='fa fa-plus-square-o'></i> Branch</span></button>
                                            <a class="collapse-link" >
                                                <i class="fa fa-chevron-up" v-on:click.stop='collapseBox'></i>
                                            </a>
                                        </div>
                                    </div>
                                    <div id="parallel">
                                        <div class="ibox-content">
                                            <div class='row'>
                                                <div class='row'><label class="headmsg control-label">Branches:</label></div>
                                                <div class='row'>
                                                    <div class='col-md-offset-1'>
                                                        <div v-for='branch in parallelBranches' class="row" style='border-left-style: solid; border-left-color: gray; margin-bottom: 20px; padding-top: 7px; padding-bottom: 7px;'>
                                                            <label class="headmsg control-label">Branch:</label>
                                                            <div class="col-md-3">
                                                                <select class="myselect chooseStep form-control" v-model='branch.orderType'>
                                                                    <option></option>
                                                                    <option v-for='orderType in ["step", "flow"]' v-bind:value='orderType'>{{ orderType }}</option>
                                                                </select>
                                                            </div>
                                                            <div class="col-md-4">
                                                                <select class="myselect chooseStep form-control" v-model='branch.orderValue'>
                                                                    <option></option>
                                                                    <option v-if='branch.orderType == "step"' v-for='stepRef in stepsRefs' v-bind:value='stepRef'>{{ stepRef }}</option>
                                                                    <option v-if='branch.orderType == "flow"' v-for='flowRef in filtedFlowsRefs' v-bind:value='flowRef'>{{ flowRef }}</option>
                                                                </select>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="ibox">
            <div class="ibox-title">
                <h5 class="text-success">OrderList</h5>
                <div class="ibox-tools">
                        <a class="collapse-link" >
                            <i class="fa fa-chevron-up" v-on:click.stop='collapseBox'></i>
                        </a>
                </div>
            </div>
            <div class="ibox-content" id="order-list">
                <div v-for='(order, index) in orderList' class='ibox float-e-margins' style='margin-bottom: 0;'>
                    <div class="ibox-title step">
                        <h5>Order #{{index+1}}   <strong style='margin-left: 20px;'>{{['normal', 'switch', 'parallel'][order.type - 1]}}</strong> </h5>
                        <div class="ibox-tools">
                            <a class="collapse-link" >
                                <i class="fa fa-chevron-up" v-on:click.stop='collapseBox'></i>
                            </a>
                            <a class="close-link" v-on:click='removeOrder'>
                                <i class="fa fa-times"></i>
                            </a>
                        </div>
                    </div>
                    <div class="ibox-content">
                        <div v-if='order.type == 1' class="row">
                            <label class="control-label" style='padding-right: 20px;'> step: </label>
                            <label class="control-label"> {{ order.step }}</label>
                        </div>
                        <div v-if='order.type == 2' class="row">
                            <div>
                                <label class="control-label" style='padding-right: 20px;'> value: </label>
                                <label class="control-label"> {{order.value}} </label>
                            </div>
                            <div><label class="control-label"> cases: </label></div>
                            <div v-for='sCase in order.cases' class="row">
                                <label class="control-label col-md-offset-1"> -- <b>{{ sCase.value }}</b> : </label>
                                <label class='coltrol-label' style='margin-left: 20px;'>{{ sCase.orderValue }} [{{ sCase.orderType }}]</label>
                            </div>
                        </div>
                        <div v-if='order.type == 3' class="row">
                            <div><label class="control-label"> </label></div>
                            <div v-for='branch in order.branches' class="row">
                                <label class="control-label col-md-offset-1" style='padding-right: 20px;'> -- branch: </label>
                                <label class="control-label"> {{ branch.orderValue }} [{{ branch.orderType }}]</label>
                            </div>
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
    name: 'flow',
    props: ['stepsRefs', 'flowsRefs', 'flowName', 'orderList'],
    model: {
        prop: 'flowName',
        event: 'editFlowName'
    },
    data: function() {
        return {
            normalStep: '',
            switchValue: '',
            switchCases: [{'value': '', 'orderType': '', 'orderValue': ''}],
            parallelBranches: [{'orderType': '', 'orderValue': ''}],
            orderSelected: 1
        }
    },
    mounted: function(){
        // this.selectPluginUpdate();
    },
    updated: function(){
        // this.selectPluginUpdate();
    },
    methods: {
        addOrder: function(){
            var select = this.orderSelected;
            if(select == 1){
                if(this.normalStep == ""){
                    alert("Not completed!!!");
                    return;
                }
                var temp = {type:1,step:this.normalStep};
                this.orderList.push(temp);
                this.normalStep = '';
            }
            if(select == 2){
                var caseList = [];
                for(var i=0; i<this.switchCases.length; ++i){
                    var caseValue = this.switchCases[i].value;
                    if(caseValue == ""){
                        alert("Not completed!!!");
                        return;
                    }
                    var caseOrderType = this.switchCases[i].orderType;
                    if(caseOrderType == ""){
                        alert("Not completed!!!");
                        return;
                    }
                    var caseOrderValue = this.switchCases[i].orderValue;
                    if(caseOrderValue == ""){
                        alert("Not completed!!!");
                        return;
                    }
                    caseList.push({value: caseValue, orderType: caseOrderType, orderValue: caseOrderValue});
                }
                temp = {type:2, value: this.switchValue, cases:caseList};
                this.orderList.push(temp);
                this.switchValue = '';
                   this.switchCases = [{value: '', orderType: '', orderValue: ''}];
            }
            if(select == 3){
                var branchList = [];
                var allStep = $('#parallel .chooseStep');
                for(var i=0; i<this.parallelBranches.length; ++i){
                    var branchOrderType = this.parallelBranches[i].orderType;
                    if(branchOrderType == ""){
                        alert("Not completed!!!");
                        return;
                    }
                    var branchOrderValue = this.parallelBranches[i].orderValue;
                    if(branchOrderValue == ""){
                        alert("Not completed!!!");
                        return;
                    }
                    branchList.push({orderType: branchOrderType, orderValue: branchOrderValue});
                }
                temp = {type:3,branches:branchList};
                this.orderList.push(temp);
                this.parallelBranches = [{orderType: '', orderValue: ''}];
            }
            this.$emit("orderList", this.orderList);
        },
        removeOrder: function(index){
            this.orderList.splice(index, 1);
        },
        addNewCase: function() {
            this.switchCases.push({value: '', orderType: '', orderValue: ''});
        },
        addNewBranch: function() {
            this.parallelBranches.push({step: ''});
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
    computed: {
        filtedFlowsRefs: function() {
            var subflowNameArr = [];
            for(var i = 0; i < this.flowsRefs.length; i++) {
                if(this.flowsRefs[i] != this.flowName) {
                    subflowNameArr.push(this.flowsRefs[i]);
                }
            }
            return subflowNameArr;
        }
    }
}
</script>
