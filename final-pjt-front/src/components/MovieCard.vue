<template>
    <div>
        <img :src="getImageUrl(movie.poster_path)" alt="Movie Poster">
        <h4>{{ movie.title }}</h4>
        <p class="overview">{{ movie.overview }}</p>
    </div>
</template>

<script setup>
defineProps(['movie'])

const getImageUrl = (posterPath) => {
    if (!posterPath) {
      return '' 
    }
    return `https://image.tmdb.org/t/p/w500/${posterPath}`
  }
</script>

<style scoped>
.overview {
  font-size: 0.6em;
}


div {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  
}

img {
  max-width: 100%;
  height: auto;
  margin-bottom: 10px;
}

h4 {
  margin-bottom: 5px;
}

p {
  margin-bottom: 0;
}

</style>