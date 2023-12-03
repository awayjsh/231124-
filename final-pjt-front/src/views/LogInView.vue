<template>
  <div class="parent">
    <h1>Login</h1>
    <div class="accounts-container">
      <form @submit.prevent="logIn">
        <label for="username">username : </label>
        <input type="text" id='username' v-model.trim="username"><br>

        <label for="password">password : </label>
        <input type="password" id='password' v-model.trim="password"><br>
        
        <div class="button-container">
          <input type="submit" value="로그인">
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>

import { ref } from 'vue'
import { useMovieStore } from '@/stores/counter.js'

const store = useMovieStore()

const username = ref(null)
const password = ref(null)

const logIn = function () {
  const payload = {
    username: username.value,
    password: password.value
  }
  store.logIn(payload)
}

</script>

<style scoped>

.parent {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.accounts-container {
  width: 600px;
  display: flex;
  justify-content: center;
  align-items: center;
  border: #000 solid 2px;
  border-radius: 2vw;
  padding: 1.8vw
}

input[type="submit"] {
  padding: 20px;
  padding-top: 5px;
  padding-bottom: 5px;
  border: 2px solid #000;
  border-radius: 4px;
  box-sizing: border-box;
  font-size: 16px;
  font-weight: bold;
  background-color: #FFD8E1;
}

.button-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 1px;
}
</style>