<template>
    <h1>장르별 영화</h1>
    <div class="center">
        <button class="buttonstyle" v-for="genre in genres" :key="genre.id" @click="getMoviesByGenre(genre.id)">
            {{ genre.name }}
        </button>
    </div>
    <hr>
    <br>
    <div class="grid-container">
        <MovieCard 
        v-for="movie in movies" 
        :key="movie.id" 
        class="card" 
        :movie="movie"
        @click="goDetail(movie.id)" />
    </div>
</template>
  
<script>

import { ref, reactive } from 'vue'
import MovieCard from '@/components/MovieCard.vue'
import { useMovieStore } from '@/stores/counter.js'
import { useRouter } from 'vue-router'

export default {
  components: {
    MovieCard,
  },
  setup() {
    const router = useRouter()
    const movieStore = useMovieStore()
    const genres = ref([
        { id: 12, name: '모험' },
        { id: 14, name: '판타지' },
        { id: 16, name: '애니메이션' },
        { id: 18, name: '드라마' },
        { id: 27, name: '공포' },
        { id: 28, name: '액션' },
        { id: 35, name: '코미디' },
        { id: 36, name: '역사' },
        { id: 37, name: '서부' },
        { id: 53, name: '스릴러' },
        { id: 80, name: '범죄' },
        { id: 99, name: '다큐멘터리' },
        { id: 878, name: 'SF' },
        { id: 9648, name: '미스터리' },
        { id: 10402, name: '음악' },
        { id: 10749, name: '로맨스' },
        { id: 10751, name: '가족' },
        { id: 10752, name: '전쟁' },
        { id: 10770, name: 'TV영화' },
    ])
    const movies = movieStore.movies

    const goDetail = (id) => {
        router.push(`/${id}`)
    }

    const getMoviesByGenreAndUpdate = async (genre_id) => {
        await movieStore.getMoviesByGenre(genre_id);
    }


    return { getMoviesByGenre: getMoviesByGenreAndUpdate, genres, movies, goDetail }
  }
}

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

hr {
  background-color: black;
  height: 2.2px;
  margin-bottom: 2vw;
  border: none;
}
.center {
  display: flex;
  justify-content: center;
  margin-bottom: 2vw;
}
</style>
  
