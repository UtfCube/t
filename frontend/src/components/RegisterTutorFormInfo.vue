<template>
  <div class="field">
    <label class="label is-large" for="degree">Ученая степень:</label>
    <div class="control">
      <input type="text" class="input is-large" id="degree" :value="value.degree" @input="update('degree', $event.target.value)">
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

@Component
export default class RsfInfo extends Vue {
    @Prop({
        type: Object
    })
    private value: any;

    update(key: any, value: any) {
        this.$emit('input', { ...this.value, [key]: value });
    }
}
</script>


<style>

</style>