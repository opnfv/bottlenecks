<template>
    <div>
        <iframe style='min-height: 700px;' height='100%' width='100%'
        v-bind:src='frameSrc'>
        </iframe>
    </div>
</template>

<script>

export default {
    data: function() {
        return {
            frameSrc: this.global.GRAFANA_ADDR
        }
    }
}
</script>

<style scoped>
</style>
