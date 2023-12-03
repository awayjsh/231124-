<template>
  <div class="parent">
    <h1>Signup</h1>
    <div class="signup">
      <form @submit.prevent="signUp">
        <label for="username">username : </label>
        <input type="text" id='username' v-model.trim="username"><br>

        <label for="password1">password : </label>
        <input type="password" id='password1' v-model.trim="password1"><br>

        <label for="password2">password confirmation : </label>
        <input type="password" id='password2' v-model.trim="password2">

        <div class="button-container">
          <input type="submit" value="회원가입">
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
const password1 = ref(null)
const password2 = ref(null)

const signUp = function () {
  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value
  }
  store.signUp(payload)
}

</script>

<style scoped>
.parent {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.signup {
  width: 700px;
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