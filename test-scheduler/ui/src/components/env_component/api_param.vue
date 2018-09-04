<template>
    <div class="row">
         <div class="form-group">
            <label class="col-lg-3 control-label">Params</label>
            <div class="col-lg-2">
                <button type="button" class="btn btn-primary btn-sm" v-on:click="addNewParam()">New</button>
            </div>
         </div>
         <div class="form-group">
            <div class="col-lg-offset-2 col-lg-8">
                <div class="table-responsive">
                 <table class="table table-bordered text-center">
                    <thead>
                        <tr>
                            <th>name</th>
                            <th class="text-center">description</th>
                            <th class="text-center">operation</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="param in params">
                            <td><input type="text" class="form-control text-center" style="border: 0px" v-model="param['name']"></td>
                            <td><input type="text" class="form-control text-center" style="border: 0px" v-bind:title="param['description']" v-model="param['description']"></td>
                            <td>
                                <button type="button" class="btn btn-white" v-on:click="deleteParam(param['name'])">
                                    <i class="fa fa-trash"></i>
                                </button>
                            </td>
                        </tr>
                    </tbody>
                 </table>
                </div>
             </div>
          </div>
     </div>
</template>
<script>
export default {
    props: ["params"],
    data: function() {
        return {
            paramArr: this.params
        }
    },
    watch: {
        paramArr: function(){
            this.$emit("params", this.paramArr);
        }
    },
    methods: {
        addNewParam: function() {
            this.params.push({'name': '', 'description': ''});
        },
        deleteParam: function(paramName) {
            for(var i = 0;i < this.params.length; i++) {
                if(paramName == this.params[i]['name']) {
                    this.params.splice(i, 1);
                }
            }
        }
    }
}
</script>
