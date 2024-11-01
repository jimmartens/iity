<template>
    <div>
      <div class="bg-white shadow rounded-lg p-6">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-xl font-bold">Thanks</h2>
          <h3 class="text-sm text-gray-500">for entering the acronym guessing game</h3>
          <router-link 
          to="/guesses/new" 
          class="inline-block px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          Guess again?
        </router-link>
        <router-link 
          to="/guesses/meaning" 
          class="inline-block px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          What does it all mean anyway?
        </router-link>
        <router-link 
          to="/guesses/view" 
          class="inline-block px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          View Other Guesses
        </router-link>
        </div>
      </div>
    </div>
</template>
