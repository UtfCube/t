<template>
    <div>
        <section class="hero is-primary">
            <div class="hero-body">
                <div class="container has-text-centered">
                    <h2 class="title">Здравствуйте, {{ username }}</h2>
                    <p class="subtitle error-msg">{{ error }}</p>
                </div>
            </div>
        </section>
        <section>
            <b-table 
                :data="info"
                :selected.sync="selected" 
                :hoverable="true" 
                :striped="true"
                focusable
                paginated
                per-page="5"
                detailed
                >
                <template slot-scope="props">
                    <b-table-column label="Имя преподавателя">
                        {{ props.row.name }}
                    </b-table-column>

                    <b-table-column label="Предмет">
                       {{ props.row.subject }}
                    </b-table-column>
                </template>
                <template slot="detail" slot-scope="details">
                    <b-table :data="checkpoints"
                        :hoverable="true" 
                        :striped="true">
                        <template slot-scope="props">
                            <b-table-column label="Контрольная точка">
                                {{ props.row.name }}
                            </b-table-column>

                            <b-table-column label="Оценка">
                                {{ props.row.mark }}
                            </b-table-column>

                            <b-table-column label="Срок сдачи">
                                {{ props.row.date }}
                            </b-table-column>
                        </template>
                    </b-table>
                </template>
            </b-table>
        </section>
    </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

@Component
export default class StudentHome extends Vue {
    private error: string = '';
    private info: any = [
        {
            name: "t t t",
            subject: "математика"
        },
        {
            name: "t t t",
            subject: "алгебра"
        }
    ]

    private checkpoints: any = [
        {
            name: "ЛР10",
            mark: "",
            date: "дд.мм.гггг"
        },
        {
            name: "ЛР1",
            mark: "",
            date: "дд.мм.гггг"
        },
        {
            name: "ЛР2",
            mark: 5,
            date: "2018-01-19"
        },
        {
            name: "ЛР3",
            mark: "",
            date: "дд.мм.гггг"
        },
        {
            name: "ЛР4",
            mark: "",
            date: "дд.мм.гггг"
        },
        {
            name: "ЛР5",
            mark: "",
            date: "дд.мм.гггг"
        },
        {
            name: "ЛР6",
            mark: "",
            date: "дд.мм.гггг"
        }
    ]

    get username() {
        return this.$store.state.userData.username;
    }

    /*get info() {
        return this.$store.state.userData.info;
    }*/

    beforeMount () {
        const error = this.$store.dispatch('getStudentHome');
    }

    click(subject: any) {
        this.$router.push({ name: 'progress', params: { subject: subject}})
    }
}
</script>

