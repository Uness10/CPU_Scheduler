<template>
  <div class="min-h-screen bg-gray-50">
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <div class="flex items-center">
            <h1 class="text-2xl font-bold text-blue-600">CPU Scheduler Simulation</h1>
          </div>
          <nav class="flex space-x-4">
            <router-link to="/" class="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-200">
              Home
            </router-link>
            <router-link to="/visualization" class="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-200">
              Visualization
            </router-link>
            <router-link to="/comparison" class="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-200">
              Algorithm Comparison
            </router-link>
            <router-link to="/about" class="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-200">
              About
            </router-link>
          </nav>
        </div>
      </div>
    </header>
    <main class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
      <router-view />
    </main>
    <footer class="bg-white mt-8 py-4 border-t border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <p class="text-center text-sm text-gray-500">
          CPU Scheduler Simulation Project &copy; 2025
        </p>
      </div>
    </footer>
  </div>
</template>

<style>
/* Global styles */
</style>
