<template>
  <div class="min-h-screen">
    <h1 class="text-2xl font-bold text-gray-800 text-center">So, what are all of those acronyms about anyway?</h1>
    <p>There are three acronyms that you can see and while we know what they are, its really fun/funny to see what people come up with.</p>
    
    <div>
      <div>
        <h2>Share Your Thoughts</h2>
        <p>Please take a wack at it and guess.  Your guess will be recorded so try and keep it somewhat less than foul.</p>
        <router-link 
          to="/guesses/new"
          class="inline-block px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"      
        >
          Guess!
        </router-link>
        <router-link 
          to="/guesses/meaning"
          class="inline-block px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 text-center"
        >
          I give up! What does it mean?!?
        </router-link>
      </div>     
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home'
}
</script>