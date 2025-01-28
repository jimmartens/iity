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
              <th class="p-2 text-left">Acronym</th>
              <th class="p-2 text-left">Guess</th>
              <th class="p-2 text-left hidden sm:table-cell">Created</th>
              <th class="p-2 text-left">Votes</th>
              <th class="p-2 text-center">+</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="guess in guesses" :key="guess.id" class="guess-row border-b" @click="goToGuessDetail(guess.id)">
              <td class="p-2 text-left">{{ guess.acronym }}</td>
              <td class="p-2 text-left">{{ guess.content }}</td>
              <td class="p-2 hidden sm:table-cell">{{ guess.created_at }}</td>
              <td class="p-2 text-center">{{ guess.upvotes }}</td>
              <td><button @click.stop="upvoteGuess(guess.id)" :disabled="votedGuesses.has(guess.id)"
                  class="p-1 bg-green-500 text-white text-center rounded hover:bg-green-600 disabled:bg-gray-400 disabled:cursor-not-allowed">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd"
                      d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v2H7a1 1 0 100 2h2v2a1 1 0 102 0v-2h2a1 1 0 100-2h-2V7z"
                      clip-rule="evenodd" />
                  </svg>
                </button></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div class="mt-4 space-y-4 sm:space-y-0 sm:flex sm:justify-between sm:items-center">
      <div class="space-y-2 sm:space-y-0 sm:flex sm:items-center">
        <select id="sort-by" v-model="sortBy" @change="getGuesses" class="p-2 border rounded mr-2">
          <option value="created_at">Date</option>
          <option value="upvotes">Upvotes</option>
        </select>
        <select id="acronym-filter" v-model="acronymFilter" @change="getGuesses()" class="p-2 border rounded">
          <option value="">All</option>
          <option value="YCHJCYADFTCSO">YCHJCYADFTCSO</option>
          <option value="YCHJCYAQFTLHPB">YCHJCYAQFTLHPB</option>
          <option value="IITYWYBMAD">IITYWYBMAD</option>
        </select>
      </div>
      <div class="flex items-center justify-between sm:justify-end">
        <button :disabled="currentPage <= 1" @click="changePage(currentPage - 1)"
          class="px-3 py-1 bg-blue-500 text-white rounded disabled:bg-gray-300">
          &lt;
        </button>
        <span class="mx-2">Page {{ currentPage }} of {{ totalPages }}</span>
        <button :disabled="currentPage >= totalPages" @click="changePage(currentPage + 1)"
          class="px-3 py-1 bg-blue-500 text-white rounded disabled:bg-gray-300">
          &gt;
        </button>
      </div>
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
}

.guess-row:hover {
  background-color: #f0f0f0;  
}

@media (max-width: 640px) {
  .guess-row td {
    padding: 0.5rem 0.25rem;
  }
  
  .guess-row td:nth-child(2) {
    max-width: 150px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
}
</style>