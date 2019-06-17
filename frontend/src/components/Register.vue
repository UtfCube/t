<template>  
  <div>
    <section class="hero is-primary">
      <div class="hero-body">
        <div class="container has-text-centered">
          <h2 class="title">Регистрация</h2>
        </div>
      </div>
    </section>
    <section class="section">
      <div class="container">
        <div class="control">
            <button class="button is-large is-primary"
            v-for="(component, tab) in tabs"
            :key="tab"
            @click="currentTab = tab"
            >{{ tab }}</button>
        </div>
        <div class="field">
          <label class="label is-large" for="lastname">Фамилия:</label>
          <div class="control">
            <input type="text" class="input is-large" id="lastname" v-model="form.lastname">
          </div>
        </div>
        <div class="field">
          <label class="label is-large" for="firstname">Имя:</label>
          <div class="control">
            <input type="text" class="input is-large" id="firstname" v-model="form.firstname">
          </div>
        </div>
        <div class="field">
          <label class="label is-large" for="patronymic">Отчество:</label>
          <div class="control">
            <input type="text" class="input is-large" id="patronymic" v-model="form.patronymic">
          </div>
        </div>
        <div class="field">
          <label class="label is-large" for="rank">Воинское звание:</label>
          <div class="control">
            <input type="text" class="input is-large" id="rank" v-model="form.rank">
          </div>
        </div>
        <component v-model="form"
            :is="currentTabComponent"
        ></component>
        <div class="field">
          <label class="label is-large" for="username">Имя пользователя:</label>
          <div class="control">
            <input type="text" class="input is-large" id="username" v-model="form.username">
          </div>
        </div>
        <div class="field">
          <label class="label is-large" for="password">Пароль:</label>
          <div class="control">
            <input type="password" class="input is-large" id="password" v-model="form.password">
          </div>
        </div>
        <div class="field">
          <label class="label is-large" for="mirror_password">Повторите пароль:</label>
          <div class="control">
            <input type="password" class="input is-large" id="mirror_password" v-model="mirror_password">
          </div>
        </div>
        <div class="control">
          <a class="button is-large is-primary" @click="register">Зарегистрироваться</a>
        </div>

      </div>
    </section>
  </div>  
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { DialogError } from '@/utils';
import RtfInfo from '@/components/RegisterTutorFormInfo.vue';
import RsfInfo from '@/components/RegisterStudentFormInfo.vue';

@Component({
  components: {RtfInfo, RsfInfo}
})
export default class Register extends Vue {
  private form: any = {};
  private mirror_password: string = '';
  private currentTab: string = 'Учитель';
  private tabs: any = {
    'Учитель': ['RtfInfo', 'tutor'], 
    'Слушатель': ['RsfInfo', 'student']
  };
  private errorMsg: string = '';

  get currentTabComponent () {
    return this.tabs[this.currentTab][0]
  }

  get currentType() {
    return this.tabs[this.currentTab][1]
  }

  async register () {
    const error = await this.$store.dispatch('register', { type: this.currentType, form: this.form })
    if (error) {
        this.$dialog.alert({ ...DialogError, message: error });
      }   
    else {
      this.$router.push(`/${this.currentType}/home`);
    }
  }
}
</script>