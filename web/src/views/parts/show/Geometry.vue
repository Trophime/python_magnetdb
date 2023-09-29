<template>
  <div class="geometry">
    <div class="flex items-center space-x-2">
      <div class="font-semibold">({{geometry.type}})</div>
      <div>{{geometry.attachment.filename}}</div>
    </div>
    <div class="geometry-action-list">
      <Button @click="remove" class="geometry-action">
        <TrashIcon class="h5 w-5" />
      </Button>
      <Button class="geometry-action" @click="download">
        <DownloadIcon class="h5 w-5" />
      </Button>
    </div>
  </div>
</template>

<script>
import { TrashIcon } from '@vue-hero-icons/outline'
import { DownloadIcon } from '@vue-hero-icons/outline'
import FormInput from "@/components/FormInput";
import FormSelect from "@/components/FormSelect";
import FormUpload from "@/components/FormUpload";
import client from "@/services/client";
import * as partService from "@/services/partService";
import Button from "@/components/Button";

export default {
  name: 'Geometry',
  props: ['geometry'],
  components: {
    Button,
    TrashIcon,
    DownloadIcon,
  },
  data() {
    return {
      FormInput,
      FormSelect,
      FormUpload,
    }
  },
  methods: {
    remove() {
      return partService.deleteGeometry({ partId: this.geometry.part_id, type: this.geometry.type })
          .then(() => {
            this.$emit('removed', this.geometry)
          })
    },
    download() {
      window.open(`${client.defaults.baseURL}/api/attachments/${this.geometry.attachment.id}/download?auth_token=${this.$store.state.token}`, '_blank')
    }
  },
}
</script>

<style scoped>
.geometry {
  @apply border px-4 pr-2 block w-full shadow-sm sm:text-sm border-gray-300 border-dashed rounded-md cursor-pointer
  flex items-center justify-between h-10;
}

.geometry-action-list {
  @apply flex items-center justify-end space-x-1;
}

.geometry-action {
  @apply hover:bg-gray-200 rounded-md px-1.5 py-1;
}
</style>
