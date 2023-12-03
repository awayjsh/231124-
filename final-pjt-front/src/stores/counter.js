import { ref,computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useMovieStore = defineStore('movie', () => {
  const movies = ref([])
  const apiKey = import.meta.env.VITE_TMDB_KEY
  const API_URL = 'http://127.0.0.1:8000'
  const token = ref(null)
  const userInfo = ref(null)
  const router = useRouter()  // router 객체를 가져오는 코드 추가
  const isLogin = computed(() => {
    if (token.value === null) {
      return false
    } else {
      return true
    }
  })

  const config = {
    method: 'GET',
    headers: { accept: 'application/json', Authorization: `Bearer ${apiKey}` },
  }

  const getMovies = async function(){
    for(let i = 1; i <= 4; i++) {
      const moviesURL = `https://api.themoviedb.org/3/movie/popular?language=ko-KR&page=${i}`
      try {
        const res = await axios.get(moviesURL, config)
        movies.value = [...movies.value, ...res.data.results]
      } catch(err) {
        console.log(err)
      }
    }
  }

  const signUp = function (payload) {
    const { username, password1, password2 } = payload

    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: {
        username, password1, password2
      }
    })
      .then((res) => {
        console.log('회원가입 완료')
        const password = password1
        logIn({ username, password })
      })
      .catch((err) => {
        if (err.response && err.response.data) {
          if (err.response.data.username) {
            // 아이디 에러 처리
            alert(`아이디 에러: ${err.response.data.username}`);
          } else if (err.response.data.password1) {
            // password1 에러 처리
            alert(`비밀번호 에러: ${err.response.data.password1}`);
          } else if (err.response.data.password2) {
            // password2 에러 처리
            alert(`비밀번호 확인 에러: ${err.response.data.password2}`);
          } else {
            // 그 외의 에러 처리
            alert(JSON.stringify(err.response.data));
          }
        } else {
          alert('회원가입 중 오류가 발생했습니다.');
        }
      })
  }

  const logIn = function (payload) {
    const { username, password } = payload
  
    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: {
        username, password
      }
    })
      .then((res) => {
        token.value = res.data.key
        console.log(userInfo.value)
        getUserInfo()
        router.push({ name: 'newhome' })  // 로그인 성공 후 newhome 페이지로 이동
      })
      .catch((err) => {
        if (err.response && err.response.data) {
          if (err.response.data.username) {
            // 아이디 에러 처리
            alert(`아이디 에러: ${err.response.data.username}`);
          } else if (err.response.data.password) {
            // 비밀번호 에러 처리
            alert(`비밀번호 에러: ${err.response.data.password}`);
          } else {
            // 그 외의 에러 처리
            alert(JSON.stringify(err.response.data));
          }
        } else {
          alert('로그인 중 오류가 발생했습니다.');
        }
      })
  }

  const logOut = function () {
    token.value = null
    router.push({ name: 'home' })
  }

  // 사용자의 정보를 가져와서 로그인 시 저장
  const getUserInfo = function () {
    axios({
      method: 'get',
      url: `${API_URL}/accounts/user/`, // 실제 사용자 정보를 가져오는 API 경로로 변경
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then((res) => {
        console.log(res)
        userInfo.value = res.data
        console.log(userInfo.value.pk)
      })
      .catch((err) => {
        console.log(err)
      })
  }

  const updateReview = function (reviewId, updatedReview) {
    axios({
      method: 'put',
      url: `${API_URL}/community/${reviewId}/ud/`,
      headers: {
        Authorization: `Token ${token.value}`
      },
      data: updatedReview
    })
      .then((res) => {
        console.log('리뷰 수정 완료')
        const index = reviews.value.findIndex(review => review.id === reviewId);
        if (index !== -1) {
          reviews.value[index] = res.data; // 수정된 리뷰로 업데이트
        }
      })
      .catch((err) => {
        console.log(err.response.data)
      })
  }

  const getSortedMovies = async function(sort_num){
    const moviesURL = `${API_URL}/movies/show/${sort_num}/`
    try {
      const res = await axios.get(moviesURL, {
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      movies.value.length = 0 // 기존에 movies에 담겨있던 데이터를 제거
      movies.value.push(...res.data)
    } catch(err) {
      console.log(err)
    }
  }

  const getMoviesByGenre = async function(genre_id) {
    const moviesURL = `${API_URL}/movies/genre/${genre_id}/`
    try {
      const res = await axios.get(moviesURL, {
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      movies.value.length = 0 // 기존에 movies에 담겨있던 데이터를 제거
      movies.value.push(...res.data) // 새로운 데이터를 movies에 추가
    } catch (err) {
      console.log(err)
    }
  }

  const likeReview = async (reviewId) => {
    try {
      const response = await axios({
        method: 'post',
        url: `${API_URL}/community/${reviewId}/like/`,
        headers: {
          Authorization: `Token ${token.value}`,
        },
      })
      return response.data
    } catch (error) {
      console.error(error)
    }
  }

  const showLike = async (reviewId) => {
    try {
      const response = await axios({
        method: 'get',
        url: `${API_URL}/community/${reviewId}/like/`,
        headers: {
          Authorization: `Token ${token.value}`,
        },
      });
      return response.data;
    } catch (error) {
      console.error(error);
    }
  };

  return { movies, getMovies, getUserInfo, signUp, logIn, token, isLogin, logOut, API_URL, userInfo, updateReview, getSortedMovies, getMoviesByGenre, likeReview, showLike }
},{persist : true})
