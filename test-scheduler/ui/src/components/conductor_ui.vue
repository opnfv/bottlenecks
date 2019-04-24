<template>
  <div>
    <iframe src='http://0.0.0.0:5000/#/workflow?q=&h=&workflowTypes=&status=&start=0' id="conductor-ui"></iframe>
  </div>
</template>

<script>
  export default {
    data () {
      return {
      }
    },
    mounted () {
      /**
       * iframe adaptive display
       */
      function changeConductorUIfIframe () {
        const conductorUI = document.getElementById('conductor-ui')
        const deviceWidth = document.body.clientWidth
        const deviceHeight = document.body.clientHeight
        conductorUI.style.width = Number(deviceWidth) + 'px'
        conductorUI.style.height = Number(deviceHeight) + 'px'
      }

      changeConductorUIfIframe()

      window.onresize = function () {
        changeConductorUIfIframe()
      }
    }
  }
</script>

<style scoped>

</style>