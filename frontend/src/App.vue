<template>
  <div
    class="flex flex-col min-h-screen font-Roboto bg-weather-primary"
    >
    
    <main class="container mx-auto p-4">
      <router-view></router-view>
    </main>
    
    <nav>
      <div>
        <div>
          <div class="min-h-screen text-center">
            <router-link 
              style="margin-left: 1px; margin-right: 1px;"
              v-if="$route.name != 'Home'"
              to="/"
              class="inline-block px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
              Home
            </router-link>
            <router-link 
              style="margin-left: 1px; margin-right: 1px;"
              to="/guesses/new" 
              class="inline-block px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
              New Guess
            </router-link>
            <router-link 
              style="margin-left: 1px; margin-right: 1px;"
              v-if="$route.name != 'Home'"
              to="/guesses/view" 
              class="inline-block px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
              View Guesses
            </router-link>
            <router-link
              style="margin-left: 1px; margin-right: 1px;"
              v-if="$route.name != 'Meaning'"
              to="/guesses/meaning"
              class="inline-block px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 text-center"
            >
              What does it mean?!?
            </router-link>
          </div>
        </div>
      </div>
    </nav>
  </div>
</template>


<script setup>
  import { RouterView } from "vue-router";
</script>

<script>
export default {
  name: 'App'
}
</script>