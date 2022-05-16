<template>
  <div v-if="simulation">
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center justify-start space-x-4">
        <div class="display-1">Simulation #{{simulation.id}}</div>
        <StatusBadge :status="simulation.status">Simulation</StatusBadge>
        <StatusBadge :status="simulation.setup_status">Setup</StatusBadge>
      </div>
      <div class="flex items-center justify-end space-x-2">
        <Button class="btn btn-primary" @click="runSetup">
          Run Setup
        </Button>
        <Button class="btn btn-primary" @click="runSimulation" :disabled="simulation.setup_status !== 'done'">
          Run Simulation
        </Button>
      </div>
    </div>

    <Alert v-if="error" class="alert alert-danger mb-6" :error="error"/>

    <Card class="mb-6">
      <template #header>
        Details
      </template>

      <Form :initial-values="simulation">
        <FormField
            label="Resource"
            name="magnet"
            :component="FormSelect"
            :required="true"
            :options="resourceOptions"
            :defaultValue="simulation.resource_id"
            :disabled="true"
        />
        <FormField
            label="Method"
            name="method"
            :component="FormSelect"
            :required="true"
            :options="methodOptions"
            :disabled="true"
        />
        <FormField
            label="Model"
            name="model"
            :component="FormSelect"
            :required="true"
            :options="modelOptions"
            :disabled="true"
        />
        <FormField
            label="Geometry"
            name="geometry"
            :component="FormSelect"
            :required="true"
            :options="geometryOptions"
            :disabled="true"
        />
        <FormField
            label="Cooling"
            name="cooling"
            :component="FormSelect"
            :required="true"
            :options="coolingOptions"
            :disabled="true"
        />
        <FormField
            label="Setup Output"
            name="setup_output"
            :component="FormUpload"
            :disabled="true"
            :default-value="simulation.setup_output_attachment"
        />
        <FormField
            label="Simulation Output"
            name="output"
            :component="FormUpload"
            :disabled="true"
            :default-value="simulation.output_attachment"
        />
        <FormField
            label="Static"
            name="static"
            :component="FormInput"
            type="checkbox"
            :disabled="true"
            :checked="simulation.static"
        />
        <FormField
            label="Non-linear"
            name="non_linear"
            :component="FormInput"
            type="checkbox"
            :disabled="true"
            :checked="simulation.non_linear"
        />
      </Form>
    </Card>

<!--    <VisualisationCard :simulationId="simulation.id"></VisualisationCard>-->
  </div>
  <Alert v-else-if="error" class="alert alert-danger" :error="error"/>
</template>

<script>
import * as simulationService from '@/services/simulationService'
import Card from '@/components/Card'
import Form from "@/components/Form";
import FormField from "@/components/FormField";
import FormInput from "@/components/FormInput";
import FormSelect from "@/components/FormSelect";
import FormUpload from "@/components/FormUpload";
import Button from "@/components/Button";
import Alert from "@/components/Alert";
import VisualisationCard from "@/views/simulations/show/VisualisationCard";
import StatusBadge from "@/components/StatusBadge";

export default {
  name: 'SimulationShow',
  components: {
    StatusBadge,
    VisualisationCard,
    Alert,
    Button,
    FormField,
    Form,
    Card,
  },
  data() {
    return {
      FormInput,
      FormSelect,
      FormUpload,
      error: null,
      simulation: null,
      resourceOptions: [],
      methodOptions: ['cfpdes', 'CG', 'HDG', 'CRB'],
      modelOptions: ['thelec', 'mag', 'thmag', 'thmagel'],
      geometryOptions: ['Axi', '3D'],
      coolingOptions: ['mean', 'grad', 'meanH', 'gradH'],
    }
  },
  methods: {
    runSimulation() {
      return simulationService.runSimulation({ id: this.simulation.id })
          .then((res) => this.simulation.status = res.status)
          .catch((err) => alert(err.message))
    },
    runSetup() {
      return simulationService.runSetup({ id: this.simulation.id })
          .then((res) => this.simulation.setup_status = res.setup_status)
          .catch((err) => alert(err.message))
    },
  },
  async mounted() {
    try {
      this.simulation = await simulationService.find({id: this.$route.params.id})
      this.resourceOptions = [
        {
          name: `${this.simulation.resource.name} (${this.simulation.resource_type})`,
          value: this.simulation.resource_id,
        }
      ]
    } catch (error) {
      this.error = error
    }
  },
}
</script>
