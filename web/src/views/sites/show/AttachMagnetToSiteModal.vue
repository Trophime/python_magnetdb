<template>
  <Modal :visible="visible" @close="$emit('close')" :closeable="true">
    <template #header>
      Attach to site
    </template>
    <template>
      <Form ref="form" @submit="submit" @validate="validate">
        <FormField
            label="Magnet"
            name="magnet"
            :component="FormSelect"
            :required="true"
            :options="magnetOptions"
            @search="searchMagnet"
        />
      </Form>
    </template>
    <template #footer>
      <div class="flex items-center space-x-2">
        <Button type="button" class="btn btn-primary" @click="$refs.form.submit()">
          Attach
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
import * as siteService from '@/services/siteService'
import * as magnetService from '@/services/magnetService'
import Form from "@/components/Form";
import FormField from "@/components/FormField";
import FormSelect from "@/components/FormSelect";
import Button from "@/components/Button";
import Modal from "@/components/Modal";

export default {
  name: 'AttachMagnetToSiteModal',
  props: ['visible', 'siteId'],
  components: {
    Modal,
    Button,
    FormField,
    Form,
  },
  data() {
    return {
      FormSelect,
      magnetOptions: [],
    }
  },
  methods: {
    searchMagnet(query, loading) {
      loading(true)
      magnetService.list({ query, status: ['in_study', 'in_stock'] })
        .then((magnets) => {
          this.magnetOptions = magnets.items.map((item) => ({ name: item.name, value: item.id }))
        })
        .finally(() => loading(false))
    },
    submit(values, {setRootError}) {
      let payload = {
        siteId: this.siteId,
        magnetId: values.magnet.value,
      }

      return siteService.addMagnet(payload)
          .then(() => this.$emit('close', true))
          .catch(setRootError)
    },
    validate() {
      return Yup.object().shape({
        magnet: Yup.object().required(),
      })
    },
  },
  async mounted() {
    const magnets = await magnetService.list({ status: ['in_study', 'in_stock'] })
    this.magnetOptions = magnets.items.map((item) => ({ name: item.name, value: item.id }))
  }
}
</script>
