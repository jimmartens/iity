<template>
  <div>
    <h1><b>Take a Guess</b></h1>
    <form @submit.prevent="showValidationModal">
      <div>
        <label for="name">
          Name
        </label>
        <input id="name" v-model="name" placeholder="Your name" required class="block w-full p-2 border rounded">
      </div>
      <div class="mb-4">
        <label for="acronym">
          Which acronym?
        </label>
        <select id="acronym" v-model="acronym" required class="block w-full p-2 border rounded">
          <option value="YCHJCYADFTCSO">YCHJCYADFTCSO</option>
          <option value="YCHJCYAQFTLHPB">YCHJCYAQFTLHPB</option>
          <option value="IITYWYBMAD">IITYWYBMAD</option>
        </select>
      </div>
      <div class="mb-4">
        <label for="content">
          Guess
        </label>
        <textarea id="content" v-model="content" placeholder="Your guess" required
          class="block w-full p-2 border rounded" rows="4"></textarea>
      </div>

      <div class="flex space-x-4">
        <button type="submit" class="inline-block px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
          Submit Guess
        </button>
      </div>
    </form>
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div class="bg-white p-6 rounded-lg shadow-lg w-96">
        <h2 class="text-lg font-bold mb-4">Validation Results</h2>
        <div v-if="validationMessage" class="text-red-500 mb-4">
          {{ validationMessage }}
        </div>
        <div class="flex justify-end space-x-4">
          <button @click="showModal = false"
            class="inline-block px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600">Try Again
          </button>
          <button @click="submitGuessAnyway()"
            class="inline-block px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600">Submit Anyway
          </button>
        </div>
      </div>
    </div>

    <div v-if="error" class="mt-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
      {{ error }}
    </div>

    <div v-if="success" class="mt-4 bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
      {{ success }}
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

// Array of strings commenting on the guess being too short
const SHORT_GUESS_COMMENTS = [
  "Too short! Try making it longer.",
  "Not quite right. The acronym has more words.",
  "Are you sure? The acronym has the same number of words as the guess.",
  "Are you sure? An acronym of length ${acronym.value.length} is a bit lonely without ${acronym.value.length} words."
];

const LONG_GUESS_COMMENTS = [
  "Nice try! The acronym has less words.",
  "Hmmm, a bit wordy are we?",
]

export default {
  name: 'NewGuess',
  setup() {
    const router = useRouter();
    const name = ref('');
    const content = ref('');
    const acronym = ref('YCHJCYADFTCSO');
    const error = ref('');
    const success = ref('');
    const loading = ref(false);
    const validationMessage = ref('');
    const showModal = ref(false);
    const API_URL = import.meta.env.VITE_API_URL;

    const validateGuess = () => {
      if (!content.value) {
        validationMessage.value = "";
        return true;
      }
      const words = content.value.trim().split(/\s+/);

      if (words.length < acronym.value.length) {
        const randomIndex = Math.floor(Math.random() * SHORT_GUESS_COMMENTS.length)
        validationMessage.value = SHORT_GUESS_COMMENTS[randomIndex]
        return false;
      }

      if (words.some(word => word.length > 10)) {
        const randomIndex = Math.floor(Math.random() * LONG_GUESS_COMMENTS.length)
        validationMessage.value = LONG_GUESS_COMMENTS[randomIndex]
        return false;
      }

      for (let i = 0; i < words.length; i++) {
        if (words[i][0].toUpperCase() !== acronym.value[i].toUpperCase()) {
          validationMessage.value = `Hmm, for the word starting with ${words[i][0]}, are you sure the acronym starts with ${acronym.value[i]}?`;
          return false;
        }
      }
      validationMessage.value = "";
      return true;
    }

    const showValidationModal = () => {
      if (!validateGuess()) {
        showModal.value = true
      } else {
        submitGuessAnyway();
      }
    };

    const submitGuessAnyway = async () => {
      showModal.value = false;
      loading.value = true;
      error.value = ''
      success.value = ''
      try {
        await axios.post(`${API_URL}/guesses`, {
          name: name.value,
          content: content.value,
          acronym: acronym.value
        });
        success.value = 'Guess submitted successfully. Thanks!';
        // Clear the form
        name.value = '';
        content.value = '';
        acronym.value = 'YCHJCYADFTCSO';
        setTimeout(() => {
          router.push('/guesses/view');
        }, 2000);
      } catch (e) {
        error.value = 'Failed to submit guess: ' + (e.response?.data?.detail || e.message);
        console.error('Error submitting guess:', e);
      } finally {
        loading.value = false;
      }
    };


    return {
      name,
      content,
      acronym,
      error,
      success,
      loading,
      validationMessage,
      showModal,
      showValidationModal,
      submitGuessAnyway
    };
  },
};
</script>