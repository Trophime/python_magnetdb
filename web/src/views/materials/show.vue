<template>
  <div v-if="material">
    <div class="flex items-center justify-between mb-6">
      <div class="display-1">
        Material Definition: {{ material.name }}
      </div>
    </div>

    <Alert v-if="error" class="alert alert-danger mb-6" :error="error"/>

    <Card class="mb-6">
      <template #header>
        Details
      </template>

      <Form :initial-values="material" @submit="submit" @validate="validate">
        <FormField
            label="Name"
            name="name"
            type="text"
            :component="FormInput"
            :required="true"
        />
        <FormField
            label="Description"
            name="description"
            type="text"
            :component="FormInput"
        />
        <FormField
            label="Nuance"
            name="nuance"
            type="text"
            :component="FormInput"
        />
        <FormField
            label="RPE"
            name="rpe"
            type="number"
            :component="FormInput"
            :required="true"
        />
        <FormField
            label="T Ref"
            name="t_ref"
            type="number"
            placeholder="20"
            :component="FormInput"
        />
        <FormField
            label="Volumic Mass"
            name="volumic_mass"
            type="number"
            placeholder="0"
            :component="FormInput"
        />
        <FormField
            label="Alpha"
            name="alpha"
            type="number"
            placeholder="0"
            :component="FormInput"
        />
        <FormField
            label="Specific Heat"
            name="specific_heat"
            type="number"
            placeholder="0"
            :component="FormInput"
        />
        <FormField
            label="Electrical Conductivity"
            name="electrical_conductivity"
            type="number"
            placeholder="0"
            :component="FormInput"
        />
        <FormField
            label="Thermal Conductivity"
            name="thermal_conductivity"
            type="number"
            placeholder="0"
            :component="FormInput"
        />
        <FormField
            label="Magnet Permeability"
            name="magnet_permeability"
            type="number"
            placeholder="0"
            :component="FormInput"
        />
        <FormField
            label="Young"
            name="young"
            type="number"
            placeholder="0"
            :component="FormInput"
        />
        <FormField
            label="Poisson"
            name="poisson"
            type="number"
            placeholder="0"
            :component="FormInput"
        />
        <FormField
            label="Expansion Coefficient"
            name="expansion_coefficient"
            type="number"
            placeholder="0"
            :component="FormInput"
        />
        <Button type="submit" class="btn btn-primary">
          Save
        </Button>
      </Form>
    </Card>

    <Card>
      <template #header>
        Related Parts
      </template>

      <div class="table-responsive">
        <table>
          <thead class="bg-white">
            <tr>
              <th>Name</th>
              <th>Description</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr
                v-for="part in material.parts" :key="part.id"
                @click="$router.push({ name: 'part', params: { id: part.id } })"
                class="cursor-pointer"
            >
              <td>{{ part.name }}</td>
              <td>
                <template v-if="part.description">{{ part.description }}</template>
                <span v-else class="text-gray-500 italic">Not available</span>
              </td>
              <td>
                <StatusBadge :status="part.status"></StatusBadge>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </Card>
  </div>
  <Alert v-else-if="error" class="alert alert-danger" :error="error"/>
</template>

<script>
import * as Yup from 'yup'
import * as materialService from '@/services/materialService'
import Card from '@/components/Card'
import Form from "@/components/Form";
import FormField from "@/components/FormField";
import FormInput from "@/components/FormInput";
import FormSelect from "@/components/FormSelect";
import Button from "@/components/Button";
import Alert from "@/components/Alert";
import StatusBadge from "@/components/StatusBadge";

export default {
  name: 'MaterialShow',
  components: {
    StatusBadge,
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
      error: null,
      material: null,
    }
  },
  methods: {
    submit(values, {setRootError}) {
      const payload = {
        id: this.material.id,
        ...values,
      }

      return materialService.update(payload)
          .then(this.fetch)
          .catch(setRootError)
    },
    validate() {
      return Yup.object().shape({
        name: Yup.string().required(),
        rpe: Yup.number().required(),
      })
    },
    fetch() {
      return materialService.find({id: this.$route.params.id})
          .then((material) => {
            this.material = material
          })
          .catch((error) => {
            this.error = error
          })
    },
  },
  async mounted() {
    await this.fetch()
  },
}
</script>
