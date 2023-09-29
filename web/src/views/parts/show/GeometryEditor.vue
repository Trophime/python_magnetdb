<template>
  <div class="mb-3">
    <div class="form-field-label">
      Geometries
    </div>

    <div class="space-y-2">
      <Geometry
        v-for="geometry in part.geometries"
        :key="geometry.id"
        :geometry="geometry"
        @removed="handleGeometryRemoved"
      />
      <Button class="btn btn-default btn-small" @click="createModalVisible = true" :skipForm="true">
        Add new geometry
      </Button>
    </div>

    <Modal :visible="createModalVisible" @close="createModalVisible = false" :closeable="true">
      <template #header>
        Add new geometry
      </template>
      <template>
        <Form ref="form" @submit="submit" @validate="validate">
          <FormField label="Type" name="type" :component="FormSelect" :required="true" :options="typeOptions" />
          <FormField label="Attachment" name="attachment" :component="FormUpload" :required="true" />
        </Form>
      </template>
      <template #footer>
        <div class="flex items-center space-x-2">
          <Button type="button" class="btn btn-primary" @click="$refs.form.submit()">
            Save
          </Button>
          <Button class="btn btn-outline-default" @click="createModalVisible = false">
            Cancel
          </Button>
        </div>
      </template>
    </Modal>
  </div>
</template>

<script>
import * as Yup from "yup";
import Modal from "@/components/Modal";
import FormSelect from "@/components/FormSelect";
import FormUpload from "@/components/FormUpload";
import FormField from "@/components/FormField";
import Button from "@/components/Button";
import Form from "@/components/Form";
import Geometry from "./Geometry";
import * as partService from "@/services/partService";

export default {
  name: 'GeometryEditor',
  props: ['part'],
  data: () => ({
    FormSelect,
    FormUpload,
    error: null,
    createModalVisible: false,
  }),
  components: {
    Form,
    Modal,
    Button,
    FormField,
    Geometry,
  },
  computed: {
    typeOptions() {
      if (this.part.type === 'helix') {
        return ['default', 'salome', 'catia', 'cam', 'shape']
      } else if (this.part.type === 'supra') {
        return ['default', 'hts']
      }
      return ['default']
    },
  },
  methods: {
    validate() {
      return Yup.object().shape({
        type: Yup.mixed().required(),
        attachment: Yup.mixed().required(),
      })
    },
    submit(values, { setRootError }) {
      return partService.createGeometry({ partId: this.part.id, ...values })
          .then((res) => {
            this.createModalVisible = false
            this.part.geometries = [
                ...this.part.geometries.filter((curr) => curr.type !== res.type),
                res,
            ]
          })
          .catch(setRootError)
    },
    handleGeometryRemoved(geometry) {
      this.part.geometries = this.part.geometries.filter((curr) => curr.id !== geometry.id)
    },
  },
}
</script>

<style scoped>
.form-field-label {
  @apply block text-sm font-medium text-gray-700 mb-1;
}
</style>
