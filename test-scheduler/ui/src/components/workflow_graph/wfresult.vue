<template>
<div style="min-height: 600px; overflow-x: auto; overflow-y: auto;">
    <div id="file-section1" class="col-md-4">
      <div id="workflow-content-div">
        <div class="dark-gray-bg" style="font-size: 17px; max-width: 500px; margin: 0 auto 10px;"> WORKFLOW.JSON CONTENT</div>
        <pre class="white-pink" id="workflow-content" style="height: 600px; background-color:#f5f5f5;"></pre>
      </div>
    </div>
    <div class="col-md-8" id="graph-show-section" style="">
      <div v-show="!wfloading" style="margin-top: 10px;">
          <div style="min-height: 30px; text-align: right;">
              <button v-show="workflowId != '' && !wfCompletedFlag" class="btn" v-on:click="completeWF(1)" title="mark the status 'complete' by hand.">mark it <strong>complete</strong></button>
          </div>
          <div id="workflow-graph">
          </div>
      </div>
      <div v-show="wfloading" class="spiner-example" id="loading">
        <div class="sk-spinner sk-spinner-three-bounce">
          <div class="sk-bounce1"></div>
          <div class="sk-bounce2"></div>
          <div class="sk-bounce3"></div>
        </div>
      </div>
          <div class="row">
          <div id="iframeContainer"></div>
          <div id="workflowId" style="display:none">
              <input name="workflowId" type="hidden" v-bind:value="workflowId" />
              <input name="function" type="hidden" value="graphLoad" />
              <button id="graphloadbtn" type="button" onclick="graphLoad()"></button>
          </div>
        </div>
    </div>
</div>
</template>
<script>
export default {
    props: ['workflowId', 'wfloading', 'wfJson'],
    name: 'wfresult',
    data: function() {
        return {
            frameLoadedFlag : false,
            initalPaintFlag : false,
            RESPONSE_TIME_LIMIT : 6000,
            responseTimeCounter : 0,
            wfCompletedFlag : false,
            intervalTime : 1000,
            timer: null
        }
    },
    computed: {
        wfget: function(){
            return !this.wfloading;
        }
    },
    watch: {
        workflowId: function(val){
            console.log("############## workflowId changed! " + val);
            this.graphLoad();
        },
        wfJson: function(val){
            this.fillWfContent(val);
        }
    },
    mounted: function(){
        window.clearInterval(this.timer);
    },
    destroyed: function(){
        window.clearInterval(this.timer);
    },
    methods: {
        graphLoad: function(){
            console.log("load function activate");
            this.reset();
            this.initialPaintWFGraph();
            var self = this;
              self.timer = window.setInterval(function() {
                if(!self.initalPaintFlag) {
                  if(self.responseTimeCounter > self.RESPONSE_TIME_LIMIT) {
                    self.initialPaintWFGraph();
                    self.responseTimeCounter = 0;
                  }
                } else {
                  if(self.frameLoadedFlag || self.responseTimeCounter > self.RESPONSE_TIME_LIMIT) {
                    self.repaintWFGraph();
                    self.responseTimeCounter = 0;
                  }
                }
                self.responseTimeCounter += self.intervalTime;
            }, self.intervalTime);
        },
        reset: function(){
            this.frameLoadedFlag = false;
              this.initalPaintFlag = false;
              this.RESPONSE_TIME_LIMIT = 6000;
              this.responseTimeCounter = 0;
              this.wfCompletedFlag = false;
              var graphDiv = document.getElementById("workflow-graph");
              graphDiv.innerHTML = '';
        },
        initialPaintWFGraph: function() {
            console.log("start to initial paint");
            this.setIframeSrc();
            var iframe = document.getElementById("testFrame");
            var self = this;
             if (iframe.attachEvent) {
               iframe.attachEvent("onload", function(){
                 window.setTimeout(function(){
                    self.frameLoadedFlag = true;
                    self.initialPaint();
                    console.log("finish to initial paint");
                 }, 1000);
               });
             } else {
               iframe.onload = function(){
                window.setTimeout(function(){
                    self.frameLoadedFlag = true;
                    self.initialPaint();
                    console.log("finish to initial paint");
                 }, 1000);
               }
             }
        },
        setIframeSrc: function(){
         var iframeContainer = document.getElementById("iframeContainer");
         var iframeDiv = document.getElementById("testFrame");
         if(iframeDiv != undefined ) {
             iframeContainer.removeChild(iframeDiv);
         }
         var apiPrefix = this.global.WF_GRAPH_ADDR + "#/workflow/id/";
         var apiUrl = apiPrefix + this.workflowId;
         console.log("workflowId prop:" + this.workflowId);
         var iframeDiv = "<iframe id=\"testFrame\" width=\"0\" height=\"0\" style=\"border: none;\" src=\"" + apiUrl + "\"></iframe>";
         iframeContainer.innerHTML = iframeDiv;
         this.frameLoadedFlag = false;
        },
        initialPaint: function() {
          var iframe = document.getElementById("testFrame");
          var frameContent = iframe.contentWindow.document.getElementById("graph-ui-content");
          if(frameContent == null) return;
          this.frameLoadedFlag = true;
          var content = frameContent.cloneNode(true);
          content.id = "graph-ui-content-1";
          var graphDiv = document.getElementById("workflow-graph");
          graphDiv.appendChild(content);
          this.initalPaintFlag = true;
          this.wfloading = false;
          console.log("####################wfloading   false######################");
        },
        repaint: function() {
             var iframe = document.getElementById("testFrame");
             var frameContent = iframe.contentWindow.document.getElementById("graph-ui-content");
             if(frameContent == null) return;
             this.frameLoadedFlag = true;
             var newContent = frameContent.cloneNode(true);
             var newNodes = newContent.getElementsByClassName("node");
             var oldContent = document.getElementById("graph-ui-content-1");
             var oldNodes = oldContent.getElementsByClassName("node");
             var completeText = iframe.contentWindow.document.getElementsByClassName("ui-content")[0].getElementsByTagName("h4")[0].getElementsByTagName("span")[3].innerHTML;
             if(newNodes.length > oldNodes.length) {
              console.log("execute in new > old");
                newContent.id = "graph-ui-content-1";
                var graphDiv = document.getElementById("workflow-graph");
                graphDiv.innerHTML = '';
                graphDiv.appendChild(newContent);
             }
             else if(newNodes.length == oldNodes.length) {
                console.log("execute in new = old");
                for(var i = 0; i < newNodes.length; i++)
                {
                  var newGraph = newNodes[i].children[0];
                  var newGraphStyle = newGraph.getAttribute("style");
                  var oldGraph = oldNodes[i].children[0];
                  var oldGraphStyle = oldGraph.getAttribute("style");
                  if(newGraphStyle != oldGraphStyle) {
                    oldGraph.setAttribute("style", newGraphStyle);
                  }
                  var newText = newNodes[i].getElementsByTagName("text")[0];
                  var newTextStyle = newText.getAttribute("style");
                  var oldText = oldNodes[i].getElementsByTagName("text")[0];
                  var oldTextStyle = oldText.getAttribute("style");
                  if(oldTextStyle != newTextStyle) {
                    oldText.setAttribute("style", newTextStyle);
                  }
                }
                if(completeText == "COMPLETED") {
                    this.completeWF(5);
                }
             }
             else {
                  console.log("execute in new < old");
             }
        },
        repaintWFGraph: function() {
         this.setIframeSrc();
         var iframe = document.getElementById("testFrame");
         var self = this;
         if (iframe.attachEvent) {
           iframe.attachEvent("onload", function(){
             window.setTimeout(function(){
                self.frameLoadedFlag = true;
                self.repaint();
             }, 1000);
           });
         } else {
          iframe.onload = function(){
            window.setTimeout(function(){
                self.frameLoadedFlag = true;
                self.repaint();
             }, 1000);
          }
         }
        },
        completeWF: function(delay) {
            this.wfCompletedFlag = true;
            console.log("#####################################completed: clean the interval  " + this.timer);
            window.clearInterval(this.timer);
            var self = this;
            window.setTimeout(function() {
              self.$emit("wfComplete", true);
            }, delay*1000);
        },
        fillWfContent: function(wfContent) {
            var contentDiv = document.getElementById("workflow-content");
            contentDiv.innerHTML = wfContent;
        }
    }
}
</script>
<style scoped>
#workflow-graph {
    text-align: center;
}
#workflow-graph > div{
    display: inline-block;
}
</style>
