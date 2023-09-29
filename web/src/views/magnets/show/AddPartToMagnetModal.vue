<template>
  <Modal :visible="visible" @close="$emit('close')" :closeable="true">
    <template #header>
      Add a part
    </template>
    <template>
      <Form ref="form" @submit="submit" @validate="validate">
        <FormField
          label="Part"
          name="part"
          :component="FormSelect"
          :required="true"
          :options="partOptions"
          @search="searchPart"
        />
      </Form>
    </template>
    <template #footer>
      <div class="flex items-center space-x-2">
        <Button type="button" class="btn btn-primary" @click="$refs.form.submit()">
          Save
        </Button>
        <Button class="btn btn-outline-default" @click="$emit('close')">
          Cancel
        </Button>
      </div>
    </template>
  </Modal>
</template>

<script>
import * as Yup from 'yup'
import * as partService from '@/services/partService'
import * as magnetService from '@/services/magnetService'
import Form from "@/components/Form";
import FormField from "@/components/FormField";
import FormSelect from "@/components/FormSelect";
import Button from "@/components/Button";
import Modal from "@/components/Modal";

export default {
  name: 'AddPartToMagnetModal',
  props: ['visible', 'magnetId'],
  components: {
    Modal,
    Button,
    FormField,
    Form,
  },
  data() {
    return {
      FormSelect,
      partOptions: [],
    }
  },
  methods: {
    searchPart(query, loading) {
      loading(true)
      partService.list({ query, status: ['in_study', 'in_stock'] })
        .then((parts) => {
          this.partOptions = parts.items.map((item) => ({name: item.name, value: item.id}))
        })
        .finally(() => loading(false))
    },
    submit(values, {setRootError}) {
      let payload = {
        magnetId: this.magnetId,
        partId: values.part.value,
      }

      return magnetService.addPart(payload)
        .then(() => this.$emit('close', true))
        .catch(setRootError)
    },
    validate() {
      return Yup.object().shape({
        part: Yup.object().required(),
      })
    },
  },
  async mounted() {
    const parts = await partService.list({ status: ['in_study', 'in_stock'] })
    this.partOptions = parts.items.map((item) => ({name: item.name, value: item.id}))
  }
}
</script>
