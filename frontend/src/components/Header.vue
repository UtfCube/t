<template>
  <nav class="navbar" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
      <a
        role="button"
        class="navbar-burger burger"
        @click="showNav = !showNav"
        aria-label="menu"
        aria-expanded="false"
        data-target="navbarElements"
      >
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
      </a>
    </div>

    <div
      id="navbarElements"
      class="navbar-menu"
      :class="{ 'is-active': showNav }"
    >
      <div class="navbar-start">
        <router-link v-if="!isAuthenticated" :to="{ name: 'login' }" class="navbar-item">
          Войти
        </router-link>
        <router-link v-if="!isAuthenticated" :to="{ name: 'register' }" class="navbar-item">
          Регистрация
        </router-link>
        <router-link v-if="isAuthenticated" :to="{ name: 'logout' }" class="navbar-item">
          Выйти
        </router-link>
      </div>
    </div>
  </nav>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class Header extends Vue {
  private showNav: boolean = false;
  get isAuthenticated () {
    return this.$store.getters.isAuthenticated
  }
}
</script>


<style>
</style>
