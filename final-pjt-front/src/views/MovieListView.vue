<template>
    <div>
        <h1>Top Rated Movie List View</h1>
        <div class="grid-container">
            <MovieCard 
            v-for="movie in movies" 
            :key="movie.id" 
            class="card" 
            :movie="movie"
            @click="GoDetail(movie.id)" />
        </div>
    </div>
</template>
  
<script setup>
import MovieCard from '@/components/MovieCard.vue'
import { ref } from 'vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'


// 단순 변수 및 API
const route = useRoute()
const router = useRouter()
const movies = ref([])
const moviesURL = 'https://api.themoviedb.org/3/movie/top_rated?language=ko-KR&page=1'
const movieId = ref(route.params.id)
// const apiKey = import.meta.env.VITE_TMDB_KEY
const apiKey = import.meta.env.VITE_TMDB_KEY


// 함수들
const config = {
    method: 'GET',
    headers: { accept: 'application/json', Authorization: `Bearer ${apiKey}` },
}

//:to="{ name : 'movieDetail', params : {movieId: movie.id}}"
const GoDetail = (movie) => {
    console.log(movieId)
    router.push(`/${movie}`)
}

// axios
axios.get(moviesURL, config)
    .then((response) => {
        console.log(movies.value)
        movies.value = response.data.results
    })
    .catch((error) => {
        console.error(error)
    })

</script>
  
<style scoped>
.grid-container {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}

.card {
    border: 1px black solid;
    padding: 20px;
    border-radius: 10px;
}

.card img {
    max-width: 100%;
    height: auto;
}

h1 {
    display: flex;
    justify-content: center;
}

.item:hover {
  cursor: pointer;
  transform: scale(1.1);
}

</style>
  