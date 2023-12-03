<template>
    <div>
      <h1>Recommended View</h1>
      <button @click="getSortedMovies(1)">관람객 수</button>
      <button @click="getSortedMovies(2)">투표 수</button>
      <button @click="getSortedMovies(3)">평점 수</button>
      <div v-for="movie in movies" :key="movie.id">
        <h2>{{ movie.title }}</h2>
        <p>{{ movie.overview }}</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { useMovieStore } from '@/stores/counter.js'
  
  const { getSortedMovies, movies } = useMovieStore()
  </script>
  
  <style scoped>
  
  </style>