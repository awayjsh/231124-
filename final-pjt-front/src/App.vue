<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useMovieStore } from '@/stores/counter.js'

const store = useMovieStore()
const logOut = () => store.logOut()
</script>

<template>
  <div class="pinkbackground">
    <div class="image-container">
    <router-link to="/">
      <img src="@/assets/image.png" alt="hi error :(">
    </router-link>
  </div>
    <nav>
      <RouterLink to="/new-home" exact-active-class="custom-active-link">Home</RouterLink>
      <!-- <RouterLink to="/movies">Top Rated Movies</RouterLink> -->
      <!-- <RouterLink to="/:movieId">movieDetail</RouterLink> -->
      <RouterLink to="/genre-search" exact-active-class="custom-active-link">Genre</RouterLink>
      <!-- <RouterLink to="/recommended">recommended</RouterLink> -->
      <RouterLink :to="{name:'SignUpView'}" exact-active-class="custom-active-link">SignUpPage</RouterLink>
      <RouterLink v-if="!store.isLogin" :to="{ name: 'LogInView' }" exact-active-class="custom-active-link">LogIn</RouterLink>
      <a v-else @click="logOut">Logout</a>
    </nav>
    <RouterView />
  </div>
</template>

<style scoped>
body,
html {
  height: 100vh;
  /* width: 100vw; */
  margin: 0;
  background-color: #FFD8E1;
}

.pinkbackground {
  padding: 5vw;
  background-color: #FFD8E1 ;
}

.image-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 2rem;
}

header {
  line-height: 1.5;
  max-height: 100vh;
}

nav {
  width: 100%;
  font-size: 25px;
  text-align: center;
  margin-top: 2rem;
  display: flex;
  justify-content: center;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}

a {
  color: #000000;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

.custom-active-link {
  color: #E12323;
}

</style>
