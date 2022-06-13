<template>
  <div class="badge" :class="{
    'badge-primary': ['in_stock', 'in_study'].includes(status),
    'badge-danger': ['defunct', 'failed'].includes(status),
    'badge-success': ['in_operation', 'in_progress', 'done'].includes(status),
    'badge-default': !['in_stock', 'in_study', 'in_operation', 'defunct', 'done', 'in_progress', 'failed'].includes(status),
  }">
    <slot></slot>
    {{ status | statusName }}
  </div>
</template>

<script>
export default {
  name: 'StatusBadge',
  props: ['status'],
}
</script>
