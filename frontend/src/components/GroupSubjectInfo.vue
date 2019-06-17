<template>
    <div>
        <section class="hero is-primary">
            <div class="hero-body">
                <div class="container has-text-centered">
                    <h2 class="title">Таблица успеваемости</h2>
                    <p class="subtitle">По предмету {{ $route.params.subject_name }} группы {{ $route.params.group_id }}</p>
                </div>
            </div>
        </section>
        <div class="field">
          <label class="label" for="name">Название:</label>
          <div class="control">
            <input type="text" class="input" id="name" v-model="cp_name">
          </div>
        </div>
        <div class="control">
          <a class="button is-primary" @click="addCheckpoint">Добавить контрольную точку</a>
        </div>
        <section>
            <b-table
                :data="newCheckpoints">
                <template slot-scope="props">
                    <b-table-column field="name" label="Название">
                        {{ props.row.name }}
                    </b-table-column>
                </template>
            </b-table>
        </section>
        <div class="control">
          <a class="button is-primary" @click="saveCheckpoints">Сохранить контрольные точки</a>
        </div>
        <section>
            <!--<b-table 
                :data="table"
                :selected.sync="selected" 
                :hoverable="true" 
                :striped="true"
                focusable
                paginated
                per-page="5"
                >
                <template slot-scope="props">
                    <b-table-column label="Имя">
                        {{ props.row.lastname + ' ' + props.row.firstname + ' ' + props.row.patronymic }}
                    </b-table-column>
                    
                    <b-table-column v-for="(value, key, index) in props.row.progress"
                        :key="index"
                        :label="key">
                        <b-table :data="[value]">
                            <template slot-scope="iprops">
                                <b-table-column v-for="(ivalue, ikey, iindex) in iprops.row"
                                :key="iindex"
                                :label="ikey">
                                    {{ ivalue }}
                                </b-table-column>
                            </template>
                        </b-table>
                    </b-table-column>
                </template>
            </b-table>-->
            <p class="control">
                <button v-if="!edit" class="button is-primary" @click="edit = !edit">Редактировать таблицу</button>
                <button v-else class="button is-primary" @click="edit = !edit">Завершить редактирование</button>
            </p>
            <b-table 
                :data="checkpoints"
                :selected.sync="selected" 
                :hoverable="true" 
                :striped="true"
                focusable
                paginated
                per-page="5"
                detailed
                >
                <template slot-scope="props">
                    <b-table-column field="name" label="Название">
                        {{ props.row.name }}
                    </b-table-column>
                </template>
                <template slot="detail" slot-scope="details">
                    <b-table v-if="edit" :data="getProgressByCheckpoint(details.row.name)"
                        :hoverable="true" 
                        :striped="true">
                        <template slot-scope="props">
                            <b-table-column label="Имя">
                                {{ props.row.lastname + ' ' + props.row.firstname + ' ' + props.row.patronymic }}
                            </b-table-column>
                            
                            <b-table-column label="Оценка">
                                <CheckpointInfo v-model="props.row.progress" property="mark" btype="number"/>
                            </b-table-column>                          
                             
                            <b-table-column label="Число попыток сдачи">
                                <CheckpointInfo v-model="props.row.progress" property="attempts" btype="number"/>   
                            </b-table-column>

                            <b-table-column label="Дата сдачи">
                                <CheckpointInfo v-model="props.row.progress" property="checkpoint_date" btype="date"/>    
                            </b-table-column>

                            <b-table-column label="Срок сдачи">
                                <CheckpointInfo v-model="props.row.progress" property="deadline" btype="date"/>    
                            </b-table-column>

                            <b-table-column label="Признаки плагиата">
                                <CheckpointInfo v-model="props.row.progress" property="plagiarism" btype="text"/>    
                            </b-table-column>
                        </template>
                    </b-table>
                    <b-table v-else :data="getProgressByCheckpoint(details.row.name)"
                        :hoverable="true" 
                        :striped="true">
                        <template slot-scope="props">
                            <b-table-column label="Имя">
                                {{ props.row.lastname + ' ' + props.row.firstname + ' ' + props.row.patronymic }}
                            </b-table-column>

                            <b-table-column label="Оценка">
                                {{ props.row.progress.mark }}
                            </b-table-column>                          
                             
                            <b-table-column label="Число попыток сдачи">
                                {{ props.row.progress.attempts }}
                            </b-table-column>

                            <b-table-column label="Дата сдачи">
                                {{ props.row.progress.checkpoint_date }}
                            </b-table-column>

                            <b-table-column label="Срок сдачи">
                                {{ props.row.progress.deadline }}
                            </b-table-column>

                            <b-table-column label="Признаки плагиата">
                                {{ props.row.progress.plagiarism }}
                            </b-table-column>
                        </template>
                    </b-table>
                </template>
            </b-table>
            <p class="control">
                <button v-if="edit" class="button is-primary" @click="updateGradesTable">Сохранить изменения</button>
            </p>
        </section>
    </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import CheckpointInfo from './CheckpointInfo.vue';
import { DialogError } from '@/utils';

@Component({
    components: {CheckpointInfo}
})
export default class GroupSubjectInfo extends Vue {
    private newProgress: any = {};
    private cp_name: string = "";
    private newCheckpoints: any[] = [];
    private selected: any = {};
    private edit: boolean = false;
    
    async beforeMount() {
        let error = await this.$store.dispatch('getCheckpoints', this.$route.params);
        if (error) {
            this.$dialog.alert({ ...DialogError, message: error });
        }
        error = await this.$store.dispatch('getGradesTable', this.$route.params);
        if (error) {
            this.$dialog.alert({ ...DialogError, message: error });
        }
    }

    get checkpoints() {
        return this.$store.state.currentCheckpoints;
    }

    getProgressByCheckpoint(checkpoint: string) {
        this.newProgress[checkpoint] = this.$store.getters.getProgressByCheckpoint(checkpoint);
        return this.newProgress[checkpoint];
    }

    addCheckpoint() {
        this.newCheckpoints.push({ name: this.cp_name})
    }

    async saveCheckpoints() {
        const error = await this.$store.dispatch('addCheckpoints', { ...this.$route.params, checkpoints: this.newCheckpoints });
        if (error) {
            this.$dialog.alert({ ...DialogError, message: error });
        }
    }

    async updateGradesTable() {
        const error = await this.$store.dispatch('updateGradesTable', { ...this.$route.params, newProgress: this.newProgress })
        if (error) {
            this.$dialog.alert({ ...DialogError, message: error });
        }
    }
}
</script>
