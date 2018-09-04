<template>
    <div class="form-group">
        <label class="col-lg-3 control-label">{{ name }}</label>
        <div class="col-lg-7">
            <input type="text" class="form-control" v-bind:value="value" v-on:input="$emit('input', $event.target.value)">
        </div>
    </div>
</template>
<script>
export default {
    props: ['name', 'value'],
    data: function() {
        return {
            inputName: this.name,
            inputValue: this.value,
            fake: "abc"
        }
    }
}
</script>
