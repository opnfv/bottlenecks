<template>
<div style="min-height: 600px; overflow-x: hidden; overflow-y: auto;">
    <div id="file-section1" class="col-md-4">
      <div id="workflow-content-div">
        <div class="dark-gray-bg" style="padding-left: 10px;font-size: 17px;"> <span> WORKFLOW.JSON CONTENT</span></div>
        <pre class="white-pink" id="workflow-content" style="height: 600px; background-color:#f5f5f5;"></pre>
      </div>
    </div>      
	<div class="col-md-offset-2 col-md-4" id="graph-show-section" style="height:600px;">
	  <div v-show="!wfloading" id="workflow-graph" style="margin-top: 10px;margin-left: 70px;">
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
import {addClass, removeClass, isContainClass} from '../../assets/js/my-util.js'
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
			var intervalTime = 1000;
			var self = this;
		  	this.timer = window.setInterval(function() {
			    if(self.wfCompletedFlag) {
			      window.clearInterval(self.timer);
			      // getWFOutput();
			    }
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
			    self.responseTimeCounter += intervalTime;
			}, intervalTime);
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
		 // var wfConfigDiv = document.getElementById("workflowId");
		 // var inputArr = wfConfigDiv.getElementsByTagName("input");
		 // var idElem = inputArr[0];
		 // var workflowId = idElem.getAttribute("value");
		 var apiUrl = apiPrefix + this.workflowId;
		 // console.log("workflowId input:" + workflowId);
		 console.log("workflowId prop:" + this.workflowId);
		 var iframeDiv = "<iframe id=\"testFrame\" width=\"0\" height=\"0\" style=\"display:none\" src=\"" + apiUrl + "\"></iframe>";
		 iframeContainer.innerHTML = iframeDiv;

		 this.frameLoadedFlag = false;
		},
		initialPaint: function() {
		  var iframe = document.getElementById("testFrame");
		  var content = iframe.contentWindow.document.getElementById("graph-ui-content").cloneNode(true); 
		  content.id = "graph-ui-content-1";
		  var graphDiv = document.getElementById("workflow-graph");
		  graphDiv.appendChild(content); 

		  this.initalPaintFlag = true;
		},
		repaint: function() {
			 var iframe = document.getElementById("testFrame");
			 var newContent = iframe.contentWindow.document.getElementById("graph-ui-content").cloneNode(true); 
			 var newNodes = newContent.getElementsByClassName("node");
			 
			 var oldContent = document.getElementById("graph-ui-content-1");
			 var oldNodes = oldContent.getElementsByClassName("node");
			 
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
			      if(i == (newNodes.length - 1) && newGraphStyle == 'stroke: #48a770; fill: #48a770') {
			          this.wfCompletedFlag = true;
			      }
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
		fillWfContent: function(wfContent) {
			var contentDiv = document.getElementById("workflow-content");
            contentDiv.innerHTML = wfContent;
		}
	}
}
</script>