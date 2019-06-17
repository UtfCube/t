<template>
    <div>
        <section class="hero is-primary">
            <div class="hero-body">
                <div class="container has-text-centered">
                    <h2 class="title">Здравствуйте, {{ username }}</h2>
                </div>
            </div>
        </section>
        <section class="section">
            <div class="container">
                <div class="field">
                    <label class="label is-large" for="subject">Предмет:</label>
                    <div class="control">
                        <input type="text" class="input is-large" id="subject" v-model="form.subject">
                    </div>
                </div>
                <div class="field">
                    <label class="label is-large" for="group">Группа:</label>
                    <div class="control">
                        <input type="text" class="input is-large" id="group" v-model="form.group">
                    </div>
                </div>
                <div class="control">
                    <a class="button is-large is-primary" @click="add">Добавить</a>
                </div>
            </div>
        </section>
        <section>
            <b-table 
                :data="assosiations"
                :selected.sync="selected" 
                :hoverable="true" 
                :striped="true"
                focusable
                @click="click">
                <template slot-scope="props">
                    <b-table-column field="group_id" label="Группа" width="80" numeric>
                        {{ props.row.group_id }}
                    </b-table-column>

                    <b-table-column field="subject_name" label="Предмет" >
                        {{ props.row.subject_name }}
                    </b-table-column>
                </template>
            </b-table>
        </section>
    </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { DialogError } from '@/utils';

@Component
export default class TutorHome extends Vue {
    private form: any = {};
    private selected: object = {};

    async beforeMount () {
        const error = await this.$store.dispatch('getTutorHome');
        if (error) {
            this.$dialog.alert({ ...DialogError, message: error });
        }
    }

    get username () {
        return this.$store.state.userData.username;
    }

    get assosiations () {
        return this.$store.state.userData.info;
    }

    async add () {
        const error = await this.$store.dispatch('addNewSubject', { group_id: this.form.group, subject_name: this.form.subject });
        if (error) {
            this.$dialog.alert({ ...DialogError, message: error });
        }
    }

    click(row: any) {
        this.$router.push({name: 'GroupSubjectInfo', params: row });
    }
}
</script>

