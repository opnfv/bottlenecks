<template>
  <div id="app">
    <div class="row border-bottom blue-bg my-page-header">
        <p id="title">OPNFV Bottlenecks Portal</p>
        <ul id="intr_table" class="nav navbar-nav">
          <li v-bind:class="{'router-link-active': cur_route == '/'}"><router-link to="/">Test Suites</router-link></li>
          <li v-bind:class="{'router-link-active': cur_route == 'result'}"><router-link to="/result">Test Results</router-link></li>
          <li v-bind:class="{'router-link-active': cur_route == 'report'}"><router-link to="/report">Reports</router-link></li>
          <li v-bind:class="{'router-link-active': cur_route == 'environment'}"><router-link to="/environment">Environments</router-link></li>
        </ul>
    </div>
    <router-view/>
  </div>
</template>
<script>
export default {
  name: 'App',
  data: function() {
    return {
      cur_route: ''
    }
  },
  watch: {
    '$route': function() {
      this.highlightLink();
    }
  },
  mounted: function() {
    this.highlightLink();
  },
  methods: {
    highlightLink: function() {
      var name = this.$route.name;
      if(name == 'result' || name == 'report' || name == 'environment') {
        this.cur_route = name;
      } else {
        this.cur_route = '/';
      }
    }
  }
}
</script>

