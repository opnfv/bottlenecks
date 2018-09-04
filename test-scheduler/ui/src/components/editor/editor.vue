<template>
<div class="col-md-offset-1 col-md-10" style="margin-top: 20px;">
    <ul class="nav nav-tabs">
        <li class="active"><a data-toggle="tab" data-target="#step-pane">Step</a></li>
        <li><a data-toggle="tab" data-target="#flow-pane">Flow</a></li>
    </ul>
    <div class="tab-content">
        <div id="step-pane" class="tab-pane active fade in">
            <br>
            <div class="row">
                <div class='col-md-12'>
                    <step v-bind:stepList="stepList" v-on:stepList="getStepList"></step>
                </div>
            </div>
        </div>
        <div id="flow-pane" class="tab-pane fade">
            <br>
            <div class="row">
                <div class='col-md-12'>
                    <div class="row">
                        <button style='margin-left:20px; margin-bottom: 30px;' class="btn btn-success" type="button" id="new-flow" v-on:click='addSubflow'>&nbsp;&nbsp;<span class="bold">ADD FLOW</span></button>
                    </div>
                    <div class='row'>
                        <div class='col-md-2'>
                            <ul id="flow-tabs">
                                <li class="active"><a data-toggle="tab" data-target="#flow-main">main</a></li>
                                <li v-for="subflow in subflowList"><a data-toggle="tab" v-bind:data-target="'#' + subflow.tabId">{{ subflow.name }}</a></li>
                            </ul>
                        </div>
                        <div class="col-md-10">
                            <div class="tab-content">
                                <div id="flow-main" class="tab-pane active fade in">
                                    <flow v-model='mainflowName' v-bind:orderList='mainOrdersList' v-bind:stepsRefs='stepNameList' v-bind:flowsRefs='flowNameList' v-on:orderList='updateOrderList($event, mainflowName)'>
                                    </flow>
                                </div>
                                <div v-for="subflow in subflowList" v-bind:id="subflow.tabId" class="tab-pane fade">
                                    <flow v-model='subflow.name' v-bind:orderList='subflow.orderList' v-bind:stepsRefs='stepNameList' v-bind:flowsRefs='flowNameList' v-on:orderList='updateOrderList($event, subflow.name)'></flow>
                                </div>
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
import '../../assets/css/editor.css'
import step from './step.vue'
import flow from './flow.vue'
import showMessage from '../message/showMessage.js'
export default {
    name: 'editor',
    props: ['saveSignal', 'stepList', 'mainOrdersList', 'subflowList'],
    model: {
        prop: 'saveSignal',
        event: 'saveResponse'
    },
    data: function(){
        return {
            mainflowName: 'main'
        }
    },
    components: {
        step,
        flow
    },
    methods: {
        getStepList: function(stepList) {
            this.stepList = stepList;
        },
        addSubflow: function() {
            var tabid = "flow-" + Math.floor(Math.random()*(1000000));
            this.subflowList.push({'tabId': tabid, 'name': 'fake', 'orderList': []});
        },
        updateOrderList: function(orderList, flowName) {
            if(flowName == 'main') {
                this.mainOrdersList = orderList;
            } else {
                for(var i = 0; i < this.subflowList.length; ++i) {
                    if(this.subflowList[i].name == flowName) {
                        this.subflowList[i].orderList = orderList;
                    }
                }
            }
        }
    },
    computed: {
        flowNameList: function() {
            var stepNameArr = [];
            for(var i = 0; i < this.subflowList.length; i++) {
                stepNameArr.push(this.subflowList[i].name);
            }
            console.log(stepNameArr);
            return stepNameArr;
        },
        stepNameList: function() {
            var stepNameArr = [];
            for(var i = 0; i < this.stepList.length; i++) {
                stepNameArr.push(this.stepList[i].name);
            }
            return stepNameArr;
        }
    },
    watch: {
        saveSignal: function(newVal) {
            if(newVal == true) {
                console.log("editor newVal true");
                var self = this;
                var msgTitle = "SAVE -- TESTCASE";
                $.ajax({
                    url: this.global.SERVER_ADDR + "testcase/save",
                    method: "POST",
                    data: {
                        suiteName:  this.$route.query.suiteName,
                        caseName: this.$route.query.caseName,
                        stepList: JSON.stringify(this.stepList),
                        subflowList: JSON.stringify(this.subflowList),
                        mainOrdersList: JSON.stringify(this.mainOrdersList)
                    },
                    success: function(data) {
                        console.log("ajax save content!");
                        if(data['code'] == 200) {
                            showMessage("success", msgTitle, "Save content successfully!");
                            self.$emit('saveResponse', true);
                        } else {
                            showMessage(data['code'], msgTitle, "Failed to save content!", data['error']);
                            self.$emit('saveResponse', false);
                        }
                    },
                    error: function(obj, status, msg) {
                        showMessage(status, msgTitle, "Failed to save content!", msg);
                        self.$emit('saveResponse', false);
                    }
                });
            }
        }
    }
}
</script>
