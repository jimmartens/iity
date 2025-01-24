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
        <table style="width: 100%;">
          <tr>
            <td>
              <p><strong>Name:</strong> {{ guess.name }}</p>
            </td><td>
              <p><strong>Created At:</strong> {{ guess.created_at }}</p>
            </td>
          </tr>
          <tr>
            <td>
              <p><strong>Acronym:</strong> {{ guess.acronym }}</p>
            </td><td>
              <p><strong>Means:</strong> {{ guess.meaning }} </p> 
            </td>
          </tr>
          <tr>
            <td colspan="2">
              <p><strong>Guess:</strong> {{ guess.content }}</p>
            </td>
          </tr>  
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toISOString().slice(0, 10)
    //return date.toISOString().slice(0, 16).replace('T', ' ')
}
const giveMeaning = (acronym) => {
  // switch statement based on acronym
  // Could use a map or something similar
  var meaning = "";
  switch(acronym) {
  case "YCHJCYADFTCSO":
    meaning = "Your curiosity has just cost you a donation for the Colorado Special Olympics.";
    break;
  case "YCHJCYAQFTLHPB":
    meaning = "You curiosity has just coust you a quarter for the Laradon Hall Piggy Bank.";
    break;
  case "IITYWYBMAD":
    meaning = "If I tell you will you buy me a drink?";
    break;
  default:
    meaning = "Acronym not found";
  }
  return meaning;
}

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
      this.guess.created_at = formatDate(this.guess.created_at);
      this.guess.meaning = giveMeaning(this.guess.acronym);
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