<template>
  <div>
    <div class="parent">
      <h1>리뷰 수정</h1>
      <div class="reviewcontainer">
        <form @submit.prevent="submitUpdateReview">
          <div>
            <label for="title">제목 : </label>
            <input type="text" id="title" v-model="title" class="reviewtext" required>
          </div>

          <div>
            <label for="content">내용 : </label>
            <textarea id="content" v-model="content" required></textarea>
          </div>

          <div class="button-container">
            <input type="submit" value="리뷰 수정">
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import axios from 'axios'
  import { useMovieStore } from '@/stores/counter.js'
  
  const store = useMovieStore()
  const route = useRoute()
  const router = useRouter()
  const API_URL = 'http://127.0.0.1:8000'
  const movieId = route.params.movieId
  const reviewId = route.params.reviewId
  
  const title = ref('')
  const content = ref('')
  
  onMounted(async () => {
    const response = await axios.get(`${API_URL}/community/${reviewId}/ud/`, {
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
    title.value = response.data.title
    content.value = response.data.content
  })
  
  const submitUpdateReview = async () => {
    store.updateReview(reviewId, { title: title.value, content: content.value })
    router.push(`/${movieId}/`)
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