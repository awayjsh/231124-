<template>
  <div>
    <h1>HOME</h1>
    <div class="center">
      <button @click="handleSort(1)">관람객 순</button>
      <button @click="handleSort(2)">투표 순</button>
      <button @click="handleSort(3)">평점 순</button>
    </div>
    <hr>
    <div class="grid-container">
      <MovieCard v-for="movie in movieStore.movies" :key="movie.id" class="card" :movie="movie"
        @click="GoDetail(movie.id)" />
    </div>
  </div>
</template>

<script setup>
import MovieCard from '@/components/MovieCard.vue'
import { useRouter } from 'vue-router'
import { useMovieStore } from '@/stores/counter.js'

const { getSortedMovies } = useMovieStore()

const router = useRouter()
const movieStore = useMovieStore()

const GoDetail = (movie) => {
  router.push(`/${movie}`)
}

const handleSort = async (sort_num) => {
  await getSortedMovies(sort_num)
}
</script>

<style scoped>
.grid-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.card {
  border: 2.3px black solid;
  padding: 20px;
  border-radius: 10px;
}

.card img {
  max-width: 100%;
  height: auto;
}

.center {
  display: flex;
  justify-content: center;
  margin-bottom: 2vw;
}

hr {
  background-color: black;
  height: 2.2px;
  margin-bottom: 2vw;
  border: none;
}

.custom-active-link {
      color: #E12323;
    }
</style>
