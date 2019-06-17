<template>
    
</template>


<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class Logout extends Vue{
    async beforeMount() {
        const error = await this.$store.dispatch('logout');
        if (!error) {
            this.$router.push({name: "login"});
        }
    }
}
</script>
