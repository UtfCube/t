<template>
    <div>
        <section class="hero is-primary">
            <div class="hero-body">
                <div class="container has-text-centered">
                    <h2 class="title">Ваши успехи {{ username }}:</h2>
                    <p class="subtitle error-msg">{{ error }}</p>
                </div>
            </div>
        </section>
        <section>
            <b-table 
                :data="progress"
                :selected.sync="selected" 
                :hoverable="true" 
                :striped="true"
                focusable>
                <template slot-scope="props">
                    <b-table-column field="name" label="Название">
                        {{ props.row.name }}
                    </b-table-column>

                    <b-table-column field="posting_date" label="Назначенная дата сдачи" centered>
                        {{ new Date(props.row.posting_date).toLocaleDateString() }}
                    </b-table-column>

                    <b-table-column field="critical_date" label="Крайняя дата сдачи" centered>
                        {{ new Date(props.row.critical_date).toLocaleDateString() }}
                    </b-table-column>

                    <b-table-column field="pass_date" label="Дата сдачи" centered>
                        {{ (props.row.pass_date) ? new Date(props.row.pass_date).toLocaleDateString() : null }}
                    </b-table-column>

                    <b-table-column field="approaches_number" label="Количество подходов" numeric>
                        {{ props.row.approaches_number }}
                    </b-table-column>
                </template>
            </b-table>
        </section>
    </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { DialogError } from '@/utils';

@Component
export default class Progress extends Vue {
    private selected: any = {};
    
    get username() {
        return this.$store.state.userData.username;
    }

    get progress() {
        return this.$store.state.progress;
    }
    
    async beforeMount() {
        const error = await this.$store.dispatch('getProgress', this.$route.params.subject);
        if (error) {
            this.$dialog.alert({ ...DialogError, message: error });
        }
    }
}
</script>
