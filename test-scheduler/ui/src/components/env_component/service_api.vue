<template>
    <div class="panel panel-success">
            <div class="panel-heading">
                <button type="button" class="btn btn-xs btn-danger pull-right" v-on:click="deleteApi(name)">Delete</button>
                <h5 class="panel-title">
                    <a data-toggle="collapse" data-parent="panelParent" v-bind:href="'#' + name + '-collapse'" style="display:block;">{{ name }}</a>
                </h5>
            </div>
            <div  v-bind:id="name + '-collapse'" class="panel-collapse collapse fade">
                <div class="panel-body">
                    <base-input name="name" v-model="name"></base-input>
                    <base-input name="method" v-model="method"></base-input>
                    <base-input name="baseuri" v-model="baseuri"></base-input>
                    <api-param v-bind:params="params"></api-param>
                    <div class="form-group" v-bind:class="{  'has-error': jsonSyntaxError}">
                        <label class="col-lg-3 control-label" id="templateLabel">
                            Template <i class="fa fa-question-circle"></i>
                        </label>
                        <div class="col-lg-7">
                            <!-- help text -->
                            <span id="tempHelp">Json格式文本，用于定义发送http请求的报文内容。示例如下：<br>( 其中 ((&lt;variable&gt;)) 为占位符，用于替换实际值 )<br>GET方式：<br>{<br> &nbsp;"uri" : "((baseuri))?name=((name))"<br>}<br>POST方式:<br>{<br> &nbsp;"uri" : "((baseuri))",<br> &nbsp;"body" : {<br>&nbsp;&nbsp;&nbsp;"name" : "((name))",<br>&nbsp;&nbsp;&nbsp;"account" : {<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"id" : "((user_name))",<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"addr" : "SH"<br>&nbsp;&nbsp;&nbsp;}<br>&nbsp;}<br>}</span>
                            <textarea class="form-control" style="min-height: 200px;" v-model="templateStr"></textarea>
                            <span class="help-block" v-show="jsonSyntaxError">Json语法错误，请检查！</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
</template>
<script>
import base_input from "./base_input.vue"
import api_param from "./api_param.vue"
import Vue from "vue"
export default {
    props: ['panelParent', 'name', 'method', 'baseuri', 'params', 'template'],
    watch: {
        name: function(val) {
            this.$emit("name", val);
        },
        method: function(val) {
            this.$emit("method", val);
        },
        baseuri: function(val) {
            this.$emit("baseuri", val);
        },
        params: function(val) {
            this.$emit("params", val);
        },
        templateStr: function(val) {
            try {
                console.log(JSON.parse(val));
                this.jsonSyntaxError = false;
                this.$emit("template", JSON.parse(val));
            } catch(err) {
                console.log("catch the exception templateStr");
                this.jsonSyntaxError = true;
            }
        }
    },
    components: {
        'base-input': base_input,
        'api-param': api_param
    },
    data: function() {
        return {
            jsonSyntaxError: false,
            templateStr: JSON.stringify(this.template, null, 2)
        };
    },
    methods: {
        deleteApi: function(apiName) {
            this.$emit("delete", apiName);
        }
    }
}
</script>
<style scoped>
#templateLabel:hover+div #tempHelp{
    display: block;
}
#tempHelp {
    display: none;
    position: absolute;
    width: 90%;
    min-height: 150px;
    background-color: #ab2d2d;
    color: white;
    transition: display 1s;
    text-align: left;
    padding: 10px 16px;
    z-index: 2;
    font-size: 10px;
    opacity: 0.9;
}
#tempHelp::after {
    content: '';
    position: absolute;
    bottom: 92%;
    right: 100%;
    margin-left: -5px;
    border-width: 5px;
    border-style: solid;
    border-color: transparent #ab2d2d transparent transparent;
}
@media(max-width:1200px) {
    #tempHelp::after {
        bottom: 100%;
        left: 5%;
        border-color: transparent transparent #ab2d2d transparent;
    }
}
</style>
