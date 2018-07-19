<template>
	<div class="modal inmodal fade" id="myModal">
        <div class="modal-dialog modal-lg">
            <div class="modal-content animated">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal">
                        <span aria-hidden="true">&times;</span><span class="sr-only">Close</span>
                    </button>
                    <h3 class="modal-title">{{type.service}}</h3>
                </div>
                <div class="modal-body">
                    <div class="row">
                        <form method="get" class="form-horizontal">
                            <div id="service-address">
                                <button class="btn btn-default">Basic</button>
                                <div class="form-group">
                                	<label class="col-sm-3 control-label">name</label>
                                	<div class="col-sm-7">
                                		<input  type="text" class="form-control service-title" v-model="type.service" placeholder="please input service name.">
                                	</div>
                                </div>
                                <div class="form-group">
                                    <label class="col-sm-3 control-label">ip</label>
                                    <div class="col-sm-7"><input type="text" class="form-control" v-model="ip"></div>
                                </div>
                                <div class="form-group">
                                    <label class="col-sm-3 control-label">port</label>
                                    <div class="col-sm-7"><input type="text" class="form-control" v-model="port"></div>
                                </div>
                            </div>
                            <div class="hr-line-dashed"></div>
                            <div id="service-apis">
                                <div id="apis-nav">
                                    <button class="btn btn-default">Apis</button>
                                </div>
                                <br />
                                <div id="api-panels" class="api col-sm-offset-1 col-sm-10">
                                    <div class="panel-group" id="accordion">
                                        <service-api v-for="api in apis" panel-parent="#accordion" v-bind="api" v-on:name="api.name = $event" v-on:method="api.method = $event" v-on:uri="api.uri = $event" v-on:params="api.params = $event" v-on:template="api.template = $event" v-on:delete="removeApi"></service-api>
                                    </div>

                                	<button type="button" class="btn btn-primary pull-right" v-on:click="addNewApi()">New</button>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-white" data-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-primary" v-on:click="save()">Save changes</button>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import service_api from "./service_api.vue";
export default {
	props: ['type'],
    data: function() {
        return {
            typeTag: this.type.tag,
            ip: "",
            port: "",
            apis: []
        }
    },
    created: function() {
    },
    watch: {
        type: {
            handler: function(newVal, oldVal) {
                console.log("###########type is changed!");
                console.log(oldVal);
                console.log(newVal);
                if(newVal.content) {
                   var content = newVal.content;
                   this.ip =  content.ip;
                   this.port = content.port;
                   this.apis = content.apis;
                   console.log(this.apis);
                } else {
                    this.resetModalData();
                }
                console.log("end!");
            },
            deep: true
        }
    },
    methods: {
        addNewApi: function() {
            var newApi = {'name': 'new', 'method': 'GET', 'uri': '', 'params': []};
            this.apis.push(newApi);
        },
        removeApi: function(name) {
            console.log("remove get!");
            console.log(name);
            for(var i = 0; i < this.apis.length; i++) {
                if(name == this.apis[i]['name']) {
                    this.apis.splice(i, 1);
                }
            }
        },
        save: function() {
            if(this.type.edit == true) {
                this.saveEdition();
            } else {
                this.saveCreation();
            }
            this.resetModalData();
            $("#myModal").modal("hide");
        },
        saveEdition: function() {
            console.log("save edit!!!");
            var self = this;
            $.ajax({
                url: this.global.SERVER_ADDR + "editService",
                method: "post",
                data: {
                    "oldName": 	self.type.originName,
                    "newName": 	self.type.service,
                    "ip": 		self.ip,
                    "port": 	self.port,
                    "apis": 	JSON.stringify(self.apis),
                },
                success: function(data) {
                    console.log("#############success edit");
                }
            });
            var edition = {
                'oldName': this.type.originName,
                'newName': this.type.service
            };
            this.$emit("service-edition", edition);
        },
        saveCreation: function() {
            console.log("save creation!!!");
            var self = this;
            $.ajax({
                url: this.global.SERVER_ADDR + "createService",
                method: "post",
                data: {
                    "name": self.type.service,
                    "ip": 	self.ip,
                    "port": self.port,
                    "apis": JSON.stringify(self.apis)
                },
                success: function(data) {
                    console.log("#############success create");
                }
            });
            this.$emit("service-creation", this.type.service);
        },
        resetModalData: function() {
            this.ip = "";
            this.port = "";
            this.apis = [];
        },
        getData: function() {
            console.log("apis:");
            for(i in this.apis) {
                console.log(this.apis[i]);
            }
        }
    },
    components: {
    	'service-api': service_api
    }
}
</script>