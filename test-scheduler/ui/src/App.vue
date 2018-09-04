<template>
  <div id="app">
    <div class="row border-bottom blue-bg my-page-header">
        <p id="title">OPNFV Bottlenecks Portal</p>
        <ul id="intr_table" class="nav navbar-nav">
          <li><router-link to="/">Test Suites</router-link></li>
          <li><router-link to="/result">Test Results</router-link></li>
          <li><router-link to="/report">Reports</router-link></li>
          <li><router-link to="/environment">Environments</router-link></li>
        </ul>
    </div>
    <router-view/>
  </div>
</template>
<script>
export default {
  name: 'App'
}
</script>
