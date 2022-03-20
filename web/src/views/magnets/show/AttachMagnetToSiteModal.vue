<template>
  <Modal :visible="visible" @close="$emit('close')" :closeable="true">
    <template #header>
      Attach to site
    </template>
    <template>
      <Form ref="form" @submit="submit" @validate="validate">
        <FormField
            label="Site"
            name="site"
            :component="FormSelect"
            :required="true"
            :options="siteOptions"
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
import Form from "@/components/Form";
import FormField from "@/components/FormField";
import FormSelect from "@/components/FormSelect";
import Button from "@/components/Button";
import Modal from "@/components/Modal";

export default {
  name: 'AttachMagnetToSiteModal',
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
      siteOptions: [],
    }
  },
  methods: {
    submit(values, {setRootError}) {
      let payload = {
        magnetId: this.magnetId,
        siteId: values.site.value,
      }

      return siteService.addMagnet(payload)
          .then(() => this.$emit('close', true))
          .catch(setRootError)
    },
    validate() {
      return Yup.object().shape({
        site: Yup.object().required(),
      })
    },
  },
  async mounted() {
    const sites = await siteService.list()
    this.siteOptions = sites.items
        .filter((item) => item.status === 'in_study')
        .map((item) => ({ name: item.name, value: item.id }))
  }
}
</script>
