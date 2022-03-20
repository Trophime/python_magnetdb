<template>
  <div class="badge" :class="{
    'badge-primary': ['in_stock', 'in_study'].includes(status),
    'badge-danger': ['defunct'].includes(status),
    'badge-success': ['in_operation'].includes(status),
    'badge-default': !['in_stock', 'in_study', 'in_operation', 'defunct'].includes(status),
  }">
    {{ status | statusName }}
  </div>
</template>

<script>
export default {
  name: 'StatusBadge',
  props: ['status'],
}
</script>
