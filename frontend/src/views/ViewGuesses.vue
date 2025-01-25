<template>
  <div>
    <div class="bg-white shadow rounded-lg p-6">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-xl font-bold">Guesses</h2>
      </div>
      <div class="mb-4">
        <label for="sort-by">Sort By:</label>
        <select id="sort-by" v-model="sortBy" @change="getGuesses" class="ml-2 p-2 border rounded">
          <option value="created_at">Date</option>
          <option value="upvotes">Upvotes</option>
        </select>
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
        <table style="width: 100%">
          <thead>
            <tr>
              <th>Acronym</th>
              <th>Guess</th>
              <th>Created</th>
              <th>Upvotes</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="guess in guesses" :key="guess.id" class="guess-row" @click="goToGuessDetail(guess.id)">
              <td>{{ guess.acronym }}</td>
              <td>{{ guess.content }}</td>
              <td>{{ guess.created_at }}</td>
              <td>{{ guess.upvotes }}</td>
              <td><button @click.stop="upvoteGuess(guess.id)" :disabled="votedGuesses.has(guess.id)"
                  class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 disabled:bg-gray-400 disabled:cursor-not-allowed">
                  Upvote
                </button></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="mt-4 text-center">
      <button :disabled="currentPage <= 1" @click="changePage(currentPage - 1)"
        class="px-4 py-2 bg-blue-500 text-white rounded disabled:bg-gray-300">
        Previous
      </button>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <button @click="getGuesses" class="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600">
        Refresh Guesses
      </button>
      <label for="acronym-filter">Filter by Acronym:</label>
      <select id="acronym-filter" v-model="acronymFilter" @change="getGuesses()" class="ml-2 p-2 border rounded">
        <option value="">All</option>
        <option value="YCHJCYADFTCSO">YCHJCYADFTCSO</option>
        <option value="YCHJCYAQFTLHPB">YCHJCYAQFTLHPB</option>
        <option value="IITYWYBMAD">IITYWYBMAD</option>
      </select>
      <button :disabled="currentPage >= totalPages" @click="changePage(currentPage + 1)"
        class="px-4 py-2 bg-blue-500 text-white rounded disabled:bg-gray-300">
        Next
      </button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router';

export default {
  name: 'ViewGuesses',
  setup() {
    const router = useRouter()
    const guesses = ref([])
    const error = ref('')
    const loading = ref(false)
    const currentPage = ref(1)
    const pageSize = ref(10)
    const total = ref(0)
    const acronymFilter = ref('')
    const sortBy = ref("created_at")
    const votedGuesses = ref(new Set())
    const API_URL = import.meta.env.VITE_API_URL
    const totalPages = computed(() => {
      return Math.ceil(total.value / pageSize.value)
    })
    const goToGuessDetail = (id) => {
      router.push({ name: 'GuessDetail', params: { id: id } });
    };

    const upvoteGuess = async (id) => {
      try {
        await axios.post(`${API_URL}/guesses/${id}/upvote`);
        votedGuesses.value.add(id);
        getGuesses(); // Refresh the guesses to show updated vote count
      } catch (e) {
        console.error('Error upvoting guess:', e);
        error.value = 'Failed to upvote guess: ' + (e.response?.data?.detail || e.message)
      }
    };

    const getGuesses = async () => {
      try {
        loading.value = true
        error.value = ''
        const response = await axios.get(`${API_URL}/guesses`, {
          params: {
            page: currentPage.value,
            pageSize: pageSize.value,
            acronym: acronymFilter.value || undefined,
            sortBy: sortBy.value
          },
        });
        guesses.value = response.data.guesses.map(guess => {
          return {
            ...guess, // Spread operator to copy all properties of guess into new object
            acronym: shortenedAcronym(guess.acronym),
            created_at: formatDate(guess.created_at)
          }
        })
        total.value = response.data.total
      } catch (e) {
        error.value = 'Failed to load guesses: ' + (e.response?.data?.detail || e.message)
        console.error('Error fetching guesses:', e);
      } finally {
        loading.value = false;
      }
    }

    const changePage = (page) => {
      if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page;
        getGuesses();
      }
    }

    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toISOString().slice(0, 10)
      //return date.toISOString().slice(0, 16).replace('T', ' ')
    }

    const shortenedAcronym = (acronym) => {
      if (!acronym) return ''
      return acronym.length > 4 ? '...' + acronym.slice(-4) : acronym
    }

    onMounted(getGuesses)

    return {
      guesses,
      error,
      loading,
      getGuesses,
      router,
      goToGuessDetail,
      currentPage,
      pageSize,
      total,
      acronymFilter,
      totalPages,
      changePage,
      upvoteGuess,
      sortBy,
      votedGuesses
    }
  }
}
</script>

<style scoped>
.guess-row {
  cursor: pointer;
  /* Make the cursor a pointer on hover */
}

.guess-row:hover {
  background-color: #f0f0f0;
  /* Add a subtle background color on hover */
}
</style>