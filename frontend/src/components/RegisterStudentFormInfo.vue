<template>
    <div>
        <div class="field">
            <label class="label is-large" for="admission_year">Год поступления:</label>
            <div class="control">
                <input type="text" class="input is-large" id="admission_year" :value="value.admission_year" @input="update('admission_year', $event.target.value)">
            </div>
        </div>
        <div class="field">
            <label class="label is-large" for="group_id">Номер группы:</label>
            <div class="control">
                <input type="text" class="input is-large" id="group_id" :value="value.group_id" @input="update('group_id', $event.target.value)">
            </div>
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

