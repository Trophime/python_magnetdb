<template>
  <div class="mx-auto w-full max-w-lg">
    <div class="display-1 text-center mb-6">
      New simulation
    </div>

    <Card>
      <Form @submit="submit" @validate="validate">
        <FormField
            label="Magnet"
            name="magnet"
            :component="FormSelect"
            :required="true"
            :options="magnetOptions"
        />
        <FormField
            label="Method"
            name="method"
            :component="FormSelect"
            :required="true"
            :options="methodOptions"
        />
        <FormField
            label="Model"
            name="model"
            :component="FormSelect"
            :required="true"
            :options="modelOptions"
        />
        <FormField
            label="Geometry"
            name="geometry"
            :component="FormSelect"
            :required="true"
            :options="geometryOptions"
        />
        <FormField
            label="Cooling"
            name="cooling"
            :component="FormSelect"
            :required="true"
            :options="coolingOptions"
        />
        <FormField
            label="Static"
            name="static"
            :component="FormInput"
            type="checkbox"
        />
        <FormField
            label="Non-linear"
            name="non_linear"
            :component="FormInput"
            type="checkbox"
        />
        <Button type="submit" class="btn btn-primary">
          Save
        </Button>
      </Form>
    </Card>
  </div>
</template>

<script>
import * as Yup from 'yup'
import * as magnetService from '@/services/magnetService'
import * as simulationService from '@/services/simulationService'
import Card from '@/components/Card'
import Form from "@/components/Form";
import FormField from "@/components/FormField";
import FormInput from "@/components/FormInput";
import FormSelect from "@/components/FormSelect";
import Button from "@/components/Button";

export default {
  name: 'SimulationNew',
  components: {
    Button,
    FormField,
    Form,
    Card,
  },
  data() {
    return {
      FormInput,
      FormSelect,
      error: null,
      methodOptions: ['cfpdes', 'CG', 'HDG', 'CRB'],
      modelOptions: ['thelec', 'mag', 'thmag', 'thmagel'],
      geometryOptions: ['Axi', '3D'],
      coolingOptions: ['mean', 'grad', 'meanH', 'gradH'],
      magnetOptions: [],
    }
  },
  methods: {
    submit(values, {setRootError}) {
      return simulationService.create({
        ...values,
        magnet: undefined,
        magnet_id: values.magnet.value,
      })
          .then((simulation) => {
            this.$router.push({ name: 'simulation', params: { id: simulation.id } })
          })
          .catch(setRootError)
    },
    validate() {
      return Yup.object().shape({
        magnet: Yup.mixed().required(),
        method: Yup.string().required(),
        model: Yup.string().required(),
        geometry: Yup.string().required(),
        cooling: Yup.string().required(),
      })
    },
  },
  async mounted() {
    const magnetsRes = await magnetService.list()
    this.magnetOptions = magnetsRes.items.map(magnet => ({
      name: magnet.name,
      value: magnet.id,
    }))
  },
}
</script>
