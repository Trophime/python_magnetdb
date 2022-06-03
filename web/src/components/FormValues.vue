<template>
  <div>
    <slot :values="form.values" />
  </div>
</template>

<script>
export default {
  name: 'FormValues',
  inject: ['form'],
}
</script>
