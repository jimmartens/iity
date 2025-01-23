import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import NewGuess from '../views/NewGuess.vue'
import ViewGuesses from '../views/ViewGuesses.vue'
import Meaning from '../views/Meaning.vue'
import GuessDetail from '../views/GuessDetail.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/guesses/new',
      name: 'NewGuess',
      component: NewGuess
    },
    {
      path: '/guesses/view',
      name: 'ViewGuesses',
      component: ViewGuesses
    },
    {
      path: '/guesses/meaning',
      name: 'Meaning',
      component: Meaning
    },
    {
      path: '/guesses/:id',
      name: 'GuessDetail',
      component: GuessDetail,
      props: true, // Allows passing the route params as props to the component
    },
  ]
})

export default router