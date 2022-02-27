<template>
  <div class="form-upload" :class="{ 'form-upload-error': hasError }" @click="openUpload">
    <input :key="inputKey" type="file" ref="input" @input="onInput" class="hidden" />
    <div v-if="fileName" class="form-upload-file">
      {{fileName}}
      <div v-if="$refs.input.files.length > 0" @click="clearFiles" class="do-not-open-upload">
        <TrashIcon class="h5 w-5" />
      </div>
      <div v-else class="do-not-open-upload" @click="downloadFile">
        <DownloadIcon class="h5 w-5" />
      </div>
    </div>
    <div v-else class="text-gray-500">
      Click here to select a file
    </div>
  </div>
</template>

<script>
import client from '@/services/client'
import { TrashIcon } from '@vue-hero-icons/outline'
import { DownloadIcon } from '@vue-hero-icons/outline'

export default {
  name: 'FormUpload',
  props: ['hasError', 'type', 'defaultValue'],
  components: {
    TrashIcon,
    DownloadIcon,
  },
  data() {
    return {
      fileName: false,
      inputKey: Date.now(),
    }
  },
  methods: {
    openUpload(event) {
      if (event.path.some(el => el.classList?.contains('do-not-open-upload'))) {
        return
      }
      this.$refs.input.click()
    },
    onInput(event) {
      this.$emit('value', event.target.files[0])
      this.fileName = event.target.files[0]?.name
      this.$forceUpdate()
    },
    clearFiles() {
      this.inputKey = Date.now()
      this.fileName = this.defaultValue?.filename
      this.$forceUpdate()
    },
    downloadFile() {
      window.open(`${client.defaults.baseURL}/api/attachments/${this.defaultValue.id}/download`, '_blank')
    },
  },
  mounted() {
    this.fileName = this.defaultValue?.filename
  },
}
</script>

<style scoped>
.form-upload {
  @apply border px-4 py-2 block w-full shadow-sm sm:text-sm border-gray-300 border-dashed rounded-md cursor-pointer
  flex justify-center h-10 flex-col;
}

.form-upload:disabled {
  @apply bg-gray-100 cursor-not-allowed;
}

.form-upload-error {
  @apply border-red-500 ring-red-500 !important;
}

.form-upload-file {
  @apply flex items-center justify-between;
}
</style>