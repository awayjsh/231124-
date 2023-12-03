<template>
  <div class="container">
    <img :src="`https://www.themoviedb.org/t/p/w300_and_h450_bestv2/${movie.poster_path}`" alt="포스터가 없어요 :(" />
    <h2>{{ movie.title }}</h2>
    <h4>개봉일 : {{ movie.release_date }}</h4>
    <h4>러닝타임 : {{ movie.runtime }}분</h4>
    <h4>TMDB 평점 : {{ movie.vote_average }}</h4>
    <h4>장르</h4>
    <ul>
      <li v-for="genre in movie.genres">{{ genre.name }}</li>
    </ul>
    <h2>줄거리</h2>
    <p style="text-align: center;">{{ movie.overview }}</p>
    <br>
    <RouterLink :to="{ name: 'CreateReviewView', params: { movieId: movie.id } }">
      [ 리뷰쓰러 가기 ]
    </RouterLink>
    <br>
    <br>
    <table class="review-table">
      <thead>
        <tr>
          <th>제목</th>
          <th>내용</th>
          <th>ID</th>
          <th>삭제/수정</th> <!-- 새로 추가한 헤더 -->
          <th>좋아요</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="review in reviews" :key="review.id">
          <td>{{ review.title }}</td>
          <td>{{ review.content }}</td>
          <td>{{ review.reviewer.username }}</td>
          <td v-if="review.reviewer.id === store.userInfo.pk">
            <button @click="deleteReview(review.id)">삭제</button>
            <router-link class="update" :to="{ name: 'UpdateReviewView', params: { movieId: movie.id, reviewId: review.id } }">
              수정
            </router-link>
          </td>
          <td v-else></td>
          <!-- 새로 추가한 열 -->
          <td>
            <div>
              <span v-if="review.like_count">{{ review.like_count }}명이 좋아합니다.</span>
              <span v-else>0명이 좋아합니다.</span>
            </div>
            <button @click="likeReview(review.id)" class="likebutton">
              <span v-if="review.is_liked">좋아요 취소 :(</span>
              <span v-else>♥ 좋아요 ♥</span>
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import axios from "axios"
import { useRouter, useRoute } from "vue-router"
import { ref, onMounted } from "vue"
import Modal from '@/components/YoutubeTrailerModal.vue'
import { useMovieStore } from '@/stores/counter.js'

const store = useMovieStore()
const reviews = ref([])  // 리뷰 데이터를 저장할 레퍼런스
const API_URL = 'http://127.0.0.1:8000'
const currentUser = ref()

const router = useRouter() // 라우터 인스턴스 가져오기
const route = useRoute()
const movieId = route.params.movieId
const movieURL = `https://api.themoviedb.org/3/movie/${movieId}?language=ko-KR`
const apiKey =
  import.meta.env.VITE_TMDB_KEY
const config = {
  method: "GET",
  headers: { accept: "application/json", Authorization: `Bearer ${apiKey}` },
}

const isModal = ref(false)
const movie = ref({})
const videoId = ref(''); // 실제 YouTube 영상 ID로 대체
const videoURI = ref('')
axios
  .get(movieURL, config)
  .then((response) => {
    movie.value = response.data;
    console.log(movie.value);
  })
  .catch((error) => {
    console.log(error);
  });

const openModal = function () {
  isModal.value = true
  const trailerURL = "https://www.googleapis.com/youtube/v3/search";
  const trailerApiKey = import.meta.env.VITE_YOUTUBE_KEY;

  const config = {
    method: "GET",
    params: {
      key: trailerApiKey,
      part: "snippet",
      type: "video",
      q: 'ssafy',
    },
  };
  axios
    .get(trailerURL, config)
    .then((response) => {
      videoId.value = response.data.items[0].id.videoId; // 실제 YouTube 영상 ID로 대체
      console.log('hi', response, videoId.value);
      videoURI.value = `https://www.youtube.com/embed/${videoId}`
    })
    .catch((error) => {
      console.log(error);
    });
};

const deleteReview = ((reviewId) => {
  axios({
    method: 'delete',
    url: `${API_URL}/community/${reviewId}/ud/`,
    headers: {
      Authorization: `Token ${store.token}`  // 헤더에 인증 토큰 포함
    }
  })
    .then(() => {
      const index = reviews.value.findIndex(review => review.id === reviewId);
      if (index !== -1) {
        reviews.value.splice(index, 1);
      }
    })
    .catch((err) => {
      console.log(err)
    })
})


const likeReview = async (reviewId) => {
  const review = reviews.value.find((review) => review.id === reviewId)
  if (!review) return
  const response = await store.likeReview(reviewId)
  review.like_count = response.count  // 서버에서 받은 좋아요 수로 업데이트
  review.like_list = response.like_list
  console.log(review.like_list)
  review.is_liked = response.like_list.includes(store.userInfo.pk)
}

onMounted(async () => {
  const response = await axios.get(`${API_URL}/community/${movieId}/`, {
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
  reviews.value = response.data.map((review) => {
    return {
      ...review,
      // is_liked: review.likers ? review.likers.includes(store.userInfo.pk) : false }
      is_liked: review.likers && review.likers.includes(store.userInfo.pk)
    }
  })
})


</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-left: 70px;
  margin-right: 70px;
}

@media (min-width: 768px) {
  .container {
    margin-left: 300px;
    margin-right: 300px;
  }
}

li {
  display: inline-block;
  margin: 20px;
}

.review-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  background-color: #FFD8E1;
  font-size: 30px;
  border-radius: 15px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.15);
}

.review-table th,
.review-table td {
  text-align: center;
  border: none;
  padding: 8px;
  color: #000;  /* 텍스트 색: 검은색 */
}

.review-table th {
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: center;
  background-color: #dbbac2;  /* 헤더 배경색 */
  color: #000;  /* 헤더 텍스트 색상 */
}

.review-table tr:nth-child(even) {
  background-color: #dbbac2;  /* 짝수 행의 배경색 */
}

.review-table tr:hover {
  background-color: #ddd;  /* 행에 마우스를 올렸을 때의 배경색을 변경합니다. */
}

.review-table button {
  background-color:transparent;
  border: none;
  color: #000;  /* 버튼의 텍스트 색상을 검정색으로 변경합니다. */
  padding: 5px 10px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 30px;
  margin: 2px 1px;
  cursor: pointer;
}

.review-table button:hover {
  background-color: #45a049;  /* 버튼에 마우스를 올렸을 때의 배경색 */
}


a:hover {
  text-decoration: underline;
}

.likebutton {
  background-color: transparent;
  border: 2px solid #000 !important;
  border-radius: 7px !important;
}

.update {
  color: #000000;
  text-decoration: none;
  font-size: 22px;
}
</style>
