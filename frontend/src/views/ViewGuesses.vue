<template>
  <div>
    <div class="bg-white shadow rounded-lg p-6">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-xl font-bold">Guesses</h2>
      </div>

      <div v-if="loading" class="text-center py-4">
        Loading Guesses...
      </div>

      <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
        {{ error }}
      </div>

      <div v-else-if="guesses.length === 0" class="text-gray-500 text-center py-4">
        No guesses yet. Be the first to guess!
      </div>

      <div v-else class="space-y-4">
        <table style="width: 100%;">
          <tbody>
          <tr><th>Name</th><th>Acronym</th><th>Guess</th><th>Created</th></tr>
            <tr
            v-for="guess in guesses" 
            :key="guess.id" 
            class="border-b last:border-b-0 py-4"
            >            
                <td>{{ guess.name }}</td> 
                <td>{{ guess.acronym }}</td>
                <td>{{ guess.content }}</td>
                <td>{{ guess.created_at }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="mt-4 text-center">
      <button 
        @click="fetchGuesses"
        class="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600"
      >
        Refresh Guesses
      </button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'ViewGuesses',
  setup() {
    const guesses = ref([])
    const error = ref('')
    const loading = ref(false)

    const API_URL = import.meta.env.VITE_API_URL
    console.log('API_URL: ', API_URL)

    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toISOString().slice(0, 16).replace('T', ' ')
    }

    const shortenedAcronym = (acronym) => {
      return acronym.length > 4? '...' + acronym.slice(-4) : acronym
    }

    const fetchGuesses = async () => {
      try {
        loading.value = true
        error.value = ''
        const response = await axios.get(`${API_URL}/guesses`)
        guesses.value = response.data.map(guess => {
          return {
            ...guess, // Spread operator to copy all properties of guess into new object
            acronym: shortenedAcronym(guess.acronym), 
            created_at: formatDate(guess.created_at)
          }
        })
      } catch (e) {
        error.value = 'Failed to load guesses: ' + (e.response?.data?.detail || e.message)
        console.error('Error fetching guesses:', e)
      } finally {
        loading.value = false
      }
    }

    onMounted(fetchGuesses)

    return {
      guesses,
      error,
      loading,
      fetchGuesses
    }
  }
}
</script>