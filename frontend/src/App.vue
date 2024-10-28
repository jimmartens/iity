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
              to="/"
              class="inline-block px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
              Home
            </router-link>
            <router-link 
              to="/guesses/new" 
              class="inline-block px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
              New Guess
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