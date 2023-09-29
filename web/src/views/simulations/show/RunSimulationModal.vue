<template>
  <Modal
    :visible="value"
    :closeable="true"
    @close="$emit('input', false)"
  >
    <template #header>
      Run simulation
    </template>
    <template>
      <Form ref="form" :initial-values="{ cores: 4 }" @submit="submit">
        <Alert v-if="error" class="alert alert-danger mb-6" :error="error"/>
        <FormField
          label="Server"
          name="serverId"
          :component="FormSelect"
          :required="true"
          :options="serverOptions"
        />
        <FormField
          label="Cores"
          name="cores"
          type="number"
          :component="FormInput"
          :required="true"
        />
      </Form>
    </template>
    <template #footer>
      <div class="flex items-center space-x-2">
        <Button type="button" class="btn btn-primary" @click="$refs.form.submit()">
          Run
        </Button>
        <Button class="btn btn-outline-default" @click="$emit('input', false)">
          Cancel
        </Button>
      </div>
    </template>
  </Modal>
</template>

<script>
import Modal from "@/components/Modal"
import FormSelect from "@/components/FormSelect"
import FormInput from "@/components/FormInput"
import FormField from "@/components/FormField";
import Alert from "@/components/Alert";
import Form from "@/components/Form";
import * as simulationService from "@/services/simulationService";
import * as serverService from "@/services/serverService";

export default {
  name: 'RunSimulationModal',
  props: ['simulationId', 'value'],
  data: () => ({
    FormSelect,
    FormInput,
    error: null,
    serverOptions: [
      { name: 'Local', value: null },
    ]
  }),
  components: {
    Form,
    Alert,
    FormField,
    Modal,
  },
  methods: {
    submit(values) {
      return simulationService.runSimulation({
        id: this.simulationId,
        serverId: values.serverId?.value,
        cores: values.cores
      })
          .then((res) => {
            this.$emit('triggered', res)
            this.$emit('input', false)
          })
          .catch((err) => {
            this.error = err
          })
    },
  },
  async mounted() {
    const res = await serverService.list()
    this.serverOptions = [
      ...this.serverOptions,
      ...res.items.map((server) => ({ name: server.name, value: server.id }))
    ]
  }
}
</script>
