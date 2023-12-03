<template>
    <div>
      <div class="parent">
      <h1>리뷰 작성</h1>
      <div class="reviewcontainer">
      <form @submit.prevent="createReview">
        <div>
          <label for="title">제목 : </label>
          <input type="text" v-model.trim="title" id="title" class="reviewtext">
        </div>
        <div>
          <label for="content">내용 : </label>
          <textarea v-model.trim="content" id="content"></textarea>
        </div>
        <div class="button-container">
          <input type="submit" value="리뷰 제출">
        </div>
      </form>
    </div>
    </div>
  </div>
  </template>

<script setup>
import { ref } from 'vue'
import { useMovieStore } from '@/stores/counter.js'
import { useRouter,useRoute } from 'vue-router'
import axios from "axios"

const title = ref(null)
const content = ref(null)
const store = useMovieStore()
const router = useRouter()
const route = useRoute()
const API_URL = 'http://127.0.0.1:8000'

const movieId = route.params.movieId

const createReview = function () {
  axios({
    method: 'post',
    url : `${API_URL}/community/${movieId}/review/`,
    data: {
        title: title.value,
      content: content.value,
      have_review_movie: movieId,
    },
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
    .then((res) => {
      // console.log(res)
      router.push(`/${movieId}`)
    })
    .catch((err) => {
        console.log(movieId)
      console.log(err.response.data)
    })
}

</script>

<style scoped>
.reviewtext {
  width: 500px;
}

.reviewcontainer {
  width: 700px;
  display: flex;
  justify-content: center;
  align-items: center;
  border: #000 solid 2px;
  border-radius: 2vw;
  padding: 1.8vw;
  height: 400px;
}

.parent {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.button-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 1px;
}
</style>