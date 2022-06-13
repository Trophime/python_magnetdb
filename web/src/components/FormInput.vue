<template>
  <input
    class="form-input"
    :class="{ 'form-input-error': hasError }"
    @input="onInput"
    :type="type"
  />
</template>

<script>
export default {
  name: 'FormInput',
  props: ['hasError', 'type'],
  methods: {
    onInput(event) {
      if (this.type === 'file') {
        this.$emit('value', event.target.files)
      } else {
        this.$emit('value', event.target.value)
      }
    }
  }
}
</script>

<style scoped>
.form-input {
  @apply focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md;
}

.form-input[type="checkbox"] {
  width: 1rem;
  height: 1rem;
}

.form-input:disabled {
  @apply bg-gray-100 cursor-not-allowed;
}

.form-input-error {
  @apply ring-1 border-red-500 ring-red-500 !important;
}
</style>
