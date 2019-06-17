<template>  
  <div>
    <section class="hero is-primary">
      <div class="hero-body">
        <div class="container has-text-centered">
          <h2 class="title">Войти</h2>
          <!--<p class="subtitle error-msg">{{ errorMsg }}</p>-->
        </div>
      </div>
    </section>
    <section class="section">
      <div class="container">
        <div class="field">
          <label class="label is-large" for="username">Имя пользователя:</label>
          <div class="control">
            <input type="text" class="input is-large" id="username" v-model="username">
          </div>
        </div>
        <div class="field">
          <label class="label is-large" for="password">Пароль:</label>
          <div class="control">
            <input type="password" class="input is-large" id="password" v-model="password">
          </div>
        </div>
        <div class="field">
            <b-checkbox v-model="type"
                true-value="student"
                false-value="tutor">
                Войти как слушатель
            </b-checkbox>
        </div>
        <div class="control">
          <a class="button is-large is-primary" @click="authenticate">Войти</a>
        </div>

      </div>
    </section>

  </div>
</template> 

<script lang="ts">
import { EventBus } from '@/utils'
import { Component, Vue } from 'vue-property-decorator';
import { DialogError } from '@/utils';

@Component
export default class Login extends Vue {
  private username: string = '';
  private password: string = '';
  private type: string = 'tutor';

  async authenticate () {
    const error = await this.$store.dispatch('login', { username: this.username, password: this.password })
    if (error) {
      this.$dialog.alert({ ...DialogError, message: error });
    }
    else {
      this.$router.push(`/${this.type}/home`);
    }
  }
}
</script>


