<template>
  <div class="card">
    <div v-if="$slots.header" class="card-header">
      <slot name="header" />
    </div>
    <div class="card-body">
      <slot />
    </div>
    <div v-if="$slots.footer" class="card-footer">
      <slot name="footer" />
    </div>
  </div>
</template>

<script>
export default {
  name: 'Card',
}
</script>


<style scoped>
.card {
  @apply block bg-white rounded-md shadow border border-gray-50 w-full;
}

.card-header {
  @apply font-semibold leading-tight text-gray-900 text-xl px-3 py-2;
}

.card-body {
  @apply p-4;
}

.card-footer {
  @apply px-4 py-3 bg-gray-50 sm:px-6;
}
</style>
