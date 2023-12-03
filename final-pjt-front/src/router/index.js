import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import NewHomeView from '@/views/NewHomeView.vue'
import MovieListView from '@/views/MovieListView.vue'
import MovieDetailView from '@/views/MovieDetailView.vue'
import GenreSearchView from '@/views/GenreSearchView.vue'
import RecommendedView from '@/views/RecommendedView.vue'
import SignUpView from '@/views/SignupView.vue'
import LogInView from '@/views/LogInView.vue'
import CreateReviewView from '@/views/CreateReviewView.vue'
import UpdateReviewView from '@/views/UpdateReviewView.vue'



const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      // 메인 페이지
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      //테스트용
      path: '/new-home',
      name: 'newhome',
      component: NewHomeView
    },
    {
      // 전체 영화 목록 페이지
      path: '/movies',
      name: 'movies',
      component: MovieListView
    },
    {
      // 영화 상세 정보 페이지
      path: '/:movieId',
      name: 'movieDetail',
      component: MovieDetailView
    },
    {
      // 장르별 영화 검색 페이지
      path: '/genre-search',
      name: 'genreSearch',
      component: GenreSearchView
    },
    {
      // 날씨 기반 영화 추천 페이지
      path: '/recommended',
      name: 'recommended',
      component: RecommendedView
    },
    {
      path: '/signup',
      name: 'SignUpView',
      component: SignUpView
    },
    {
      path: '/login',
      name: 'LogInView',
      component: LogInView
    },
    {
      path: '/:movieId',
      name: 'CreateReviewView',
      component: CreateReviewView
    },
    {
      path: '/:movieId/reviews/:reviewId/update',
      name: 'UpdateReviewView',
      component: UpdateReviewView
    },
  ]
})

import { useMovieStore } from '@/stores/counter'

router.beforeEach((to, from) => {
  const store = useMovieStore()
  if (to.name === 'NewHomeView' && !store.isLogin) {
    window.alert('로그인이 필요합니다.')
    return { name: 'LogInView' }
  }
  if ((to.name === 'SignUpView' || to.name === 'LogInView') && (store.isLogin)) {
    window.alert('이미 로그인 했습니다.')
    return { name: 'NewHomeView' }
  }
})

export default router
