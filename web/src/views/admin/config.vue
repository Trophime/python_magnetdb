<template>
  <div>
    <div class="display-1 mb-6">
      Config
    </div>

    <Card>
      <Alert v-if="error" :error="error" class="alert alert-danger" />

      <pre v-if="config" class="config-container">{{JSON.stringify(config, null, 4)}}</pre>
    </Card>
  </div>
</template>

<script>
import * as configService from '@/services/admin/configService'
import Card from '@/components/Card'

export default {
  name: 'Config',
  components: {
    Card,
  },
  data() {
    return {
      error: null,
      config: null,
    }
  },
  async mounted() {
    configService.find()
      .then((config) => {
        this.config = config
      })
      .catch((error) => {
        this.error = error
      })
  },
}
</script>

<style scoped>
.config-container {
  @apply font-sans rounded-md bg-gray-200 border border-gray-500 text-gray-700 px-4 py-2;
}
</style>
