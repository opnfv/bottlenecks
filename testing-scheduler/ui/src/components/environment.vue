<template>
<div class="wrapper wrapper-content">
	<div class="row">
        <div class="col-lg-offset-2 col-lg-8">
            <div class="ibox">
                <div class="ibox-content">
                    <h1>SUT</h1>
                    <form method="get" class="form-horizontal">
                        <div class="form-group">
                            <label class="col-lg-3 control-label">Cluster</label>
                            <div class="col-lg-5">
                                <input type="text" class="form-control" placeholder="192.168.1.1">
                            </div>
                        </div>
                        <div class="form-group">
                            <label class="col-lg-3 control-label"></label>
                            <div class="col-lg-5">
                                <input type="text" class="form-control" placeholder="192.168.1.2">
                            </div>
                        </div>
                        <div class="form-group">
                            <label class="col-lg-3 control-label"></label>
                            <div class="col-lg-5">
                                <input type="text" class="form-control" placeholder="192.168.1.3">
                            </div>
                        </div>

                        <div class="form-group">
                            <label class="col-lg-3 control-label">Config file</label>
                            <div class="col-lg-5">
                                <input type="text" class="form-control" placeholder="/openrc">
                            </div>
                            <div class="col-lg-2"><button class="btn btn-w-m btn-info">upload</button></div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <div class="row">
        <div class="col-lg-offset-2 col-lg-8">
            <div class="ibox">
                <div class="ibox-content">
                    <h1>Service</h1>
                    <div class="service-table">
                        <table id="serviceList" class="table table-bordered table-hover text-center">
                            <thead>
                                <tr>
                                    <th class="text-center">No</th>
                                    <th class="text-center">Service</th>
                                    <th class="text-center">Time</th>
                                    <th class="text-center">Operation</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="service in serviceList" v-on:click="editService(service.name)" style="cursor: pointer;">
                                    <td style="vertical-align: middle;">{{ service.id }}</td>
                                    <td style="vertical-align: middle;">{{ service.name }}</td>
                                    <td style="vertical-align: middle;">{{ service.time }}</td>
                                    <td style="vertical-align: middle;"><button type="button" class="btn btn-white" v-on:click.stop="deleteService(service.name)"><i class="fa fa-trash"></i></button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <div>
                            <button class="btn btn-lg btn-success" style="float:right;" v-on:click="addNewService()">  Add  </button>
                        </div>
                    </div>

                    <!-- modal of one service -->
                    <div class="row">
                        <service-modal v-bind:type="type" v-on:service-creation="plusAService" v-on:service-edition="editAServiceName"></service-modal>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script>
    import Vue from 'vue'
    import service_modal from "./env_component/service_modal.vue"
    
    export default {
  		name: 'environment',
        data: function() {
	        return {
	            serviceList: [],
	            type: {
	                edit: true,
	                service: "ansible",
                    tag: "default"
	            }
	        }
        },
        components: {
        	'service-modal': service_modal
        },
        created: function() {
            var self = this;
            $.ajax({
                url: this.global.SERVER_ADDR + "getAllServices",
                method: "get",
                success: function(data) {
                    if(data['code'] == 200) {
                        self.serviceList = data['result'];
                    }
                }
            });
        },
        methods: {
            addNewService: function(){
                this.type.edit = false;
                this.type.tag = "abc";
                this.type.service = null;
                this.type.originName = null;
                if(this.type.content){
                    this.type.content = null;
                }
                $("#myModal").modal("show");
            },
            plusAService: function(serviceName){
                var item = {'id': '', 'name': '', 'time': ''};
                item['id'] = this.serviceList[this.serviceList.length - 1]['id'] + 1;
                item['name'] = serviceName;
                item['time'] = '2018-01-01';
                this.serviceList.push(item);
            },
            editAServiceName: function(edition) {
                for(var i = 0;i < this.serviceList.length; i++) {
                    if(edition['oldName'] == this.serviceList[i]['name']) {
                        this.serviceList[i]['name'] = edition['newName'];
                    }
                }
            },
            editService: function(serviceName){
                this.type.edit = true;
                this.type.tag = "abc";
                this.type.service = serviceName;
                this.type.originName = serviceName;
                if(this.type.content){
                    this.type.content = null;
                }
                console.log(this.type);
                var self = this;
                $.ajax({
                    url: this.global.SERVER_ADDR + "getService",
                    method: "get",
                    data: {
                        "serviceName": serviceName
                    },
                    success: function(data) {
                        console.log("#############get service!!!");
                        self.type.tag = "heyheyhey";
                        self.type.content = data['result'];
                        self.type.originName = self.type.service;
                        console.log(self.type.content);
                        console.log("#############end!!!");
                    }
                });
                $("#myModal").modal("show");
            },
            deleteService: function(serviceName){
                $.ajax({
                    url: this.global.SERVER_ADDR + "deleteService",
                    method: "post",
                    data: {
                        "serviceName": serviceName
                    },
                    success: function(data) {
                        console.log("#############delete service!!!");
                    }
                });
                for(var i = 0;i < this.serviceList.length; i++) {
                    if(serviceName == this.serviceList[i]['name']) {
                        this.serviceList.splice(i, 1);
                    }
                }
            }
        }
    }
</script>