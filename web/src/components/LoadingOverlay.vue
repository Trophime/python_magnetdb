<template>
  <div class="root">
    <div v-if="loading" class="loader">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="animate-spin">
        <circle
            class="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            stroke-width="4"
        />
        <path
            class="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
        />
      </svg>
    </div>
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: 'LoadingOverlay',
  props: ['loading'],
}
</script>

<style scoped>
.root {
  @apply relative;
}

.loader {
  @apply absolute rounded-md flex items-center justify-center z-10 top-0 left-0 w-full h-full bg-gray-700 bg-opacity-60;
}

.loader > svg {
  @apply h-24 w-24 text-black;
}
</style>
