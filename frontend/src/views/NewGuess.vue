<template>
  <div>
    <h2>Take a Guess</h2>
    <form @submit.prevent="submitGuess">
      <div>
        <label for="name">
          Name
        </label>
        <input 
          id="name"
          v-model="name" 
          placeholder="Your name" 
          required
          class="block w-full p-2 border rounded"
        >
      </div>
      
      <div class="mb-4">
        <label for="content">
          Guess
        </label>
        <textarea 
          id="content"
          v-model="content" 
          placeholder="Your guess" 
          required
          class="block w-full p-2 border rounded"
          rows="4"
        ></textarea>
      </div>
      
      <div class="flex space-x-4">
        <button 
          type="submit"
          class="inline-block px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"         
        >
          Submit Guess
        </button>
      </div>
    </form>

    <div v-if="error" class="mt-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
      {{ error }}
    </div>

    <div v-if="success" class="mt-4 bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
      {{ success }}
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

export default {
  name: 'NewGuess',
  setup() {
    const router = useRouter()
    const name = ref('')
    const content = ref('')
    const error = ref('')
    const success = ref('')

    const API_URL = 'http://localhost:8000'

    const submitGuess = async () => {
      try {
        error.value = ''
        success.value = ''
        await axios.post(`${API_URL}/guesses`, {
          name: name.value,
          content: content.value
        })
        success.value = 'Guess submitted successfully!'
        // Clear the form
        name.value = ''
        content.value = ''
        setTimeout(() => {
          router.push('/guesses/thanks')
        }, 1500)
      } catch (e) {
        error.value = 'Failed to submit guess: ' + (e.response?.data?.detail || e.message)
        console.error('Error submitting guess:', e)
      }
    }

    return {
      name,
      content,
      error,
      success,
      submitGuess
    }
  }
}
</script>