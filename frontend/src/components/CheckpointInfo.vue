<template>
    <b-input
        :type="btype"
        :value="value[property]"
        @input="update(property, $event)"
    >
    </b-input>
</template>


<script lang="ts">
import { Component, Vue, Watch, Prop } from 'vue-property-decorator';

@Component
export default class CheckpointInfo extends Vue {
  @Prop({
    type: Object,
  })
  private value: any;
  
  @Prop({
    type: String,
  })
  private property: string;
  
  @Prop({
    type: String,
  })
  private btype: string;

  private localDate: string = '';

  update(key: any, value: any) {
    this.$emit('input', { ...this.value, [key]: value });
  }
}
</script>