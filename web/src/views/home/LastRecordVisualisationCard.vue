<template>
  <VisualisationCard
    v-if="recordId !== null"
    title="Last record"
    :record-id="recordId"
  />
</template>

<script>
import * as recordService from "@/services/recordService";
import VisualisationCard from "@/views/records/show/VisualisationCard";

export default {
  name: 'LastRecordVisualisationCard',
  components: {
    VisualisationCard,
  },
  data() {
    return {
      recordId: null,
    }
  },
  async mounted() {
    try {
      const records = await recordService.list({ page: 1, perPage: 1, sortBy: 'created_at', sortDesc: true })
      if (records.items.length === 1) {
        this.recordId = records.items[0].id
      }
    } catch (error) {
      console.error(error)
    }
  },
}
</script>
