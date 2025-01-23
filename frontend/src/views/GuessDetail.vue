<template>
  <div>
    <div class="bg-white shadow rounded-lg p-6">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-xl font-bold">Guess Details</h2>
      </div>
      <div v-if="loading" class="text-center py-4">Loading...</div>
      <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
        Error: {{ error }}
      </div>

      <div v-else class="space-y-4">
        <p><strong>Name:</strong> {{ guess.name }}</p>
        <p><strong>Acronym:</strong> {{ guess.acronym }}</p>
        <p><strong>Content:</strong> {{ guess.content }}</p>
        <p><strong>Created At:</strong> {{ guess.created_at }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'GuessDetail',
data() {
  return {
    guess: null,
    loading: true,
    error: null,
    API_URL: import.meta.env.VITE_API_URL,
  };
},
mounted() {
  this.getGuess();
},
methods: {
  async getGuess() {
    try {
      const response = await axios.get(
        `${this.API_URL}/guesses/${this.$route.params.id}`,
      );
      this.guess = response.data;
    } catch (error) {
      console.error('Error fetching guess:', error);
      this.error = 'Failed to load guess details.';
    } finally {
      this.loading = false;
    }
  },
},
};
</script>