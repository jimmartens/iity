import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import NewGuess from '../views/NewGuess.vue'
import ViewGuesses from '../views/ViewGuesses.vue'
import Thanks from '../views/Thanks.vue'
import Meaning from '../views/Meaning.vue'

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
      path: '/guesses/thanks',
      name: 'Thanks',
      component: Thanks
    },
    {
      path: '/guesses/meaning',
      name: 'Meaning',
      component: Meaning
    }
  ]
})

export default router