<template>
  <div>
    {{ messageToDisplay }}
  </div>
</template>

<script>
export default {
  name: 'Alert',
  props: ['message', 'error'],
  computed: {
    messageToDisplay() {
      if (this.error?.isAxiosError && this.error.response?.data?.detail) {
        return this.error.response.data.detail
      }
      if (this.error) {
        return this.error.message
      }
      return this.message
    },
  },
}
</script>

<style>
.alert {
  @apply rounded-md p-4;
}

.alert-danger {
  @apply bg-red-200 text-red-500 border-red-200;
}

.alert-info {
  @apply bg-blue-200 text-blue-500 border-blue-200;
}
</style>
