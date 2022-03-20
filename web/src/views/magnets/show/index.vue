<template>
  <div v-if="magnet">
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center space-x-4">
        <div class="display-1">
          Magnet Definition: {{ magnet.name }}
        </div>
        <StatusBadge :status="magnet.status"></StatusBadge>
      </div>
      <Button v-if="magnet.status === 'in_stock'" class="btn btn-danger" type="button" @click="defunct">
        Defunct
      </Button>
    </div>

    <Alert v-if="error" class="alert alert-danger mb-6" :error="error"/>

    <Card class="mb-6">
      <template #header>
        Details
      </template>

      <Form :initial-values="magnet" @submit="submit" @validate="validate">
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
            label="Design Office Reference"
            name="design_office_reference"
            type="text"
            :component="FormInput"
        />
        <FormField
            label="CAO"
            name="cao"
            type="file"
            :component="FormUpload"
            :default-value="magnet.cao"
        />
        <FormField
            label="Geometry"
            name="geometry"
            type="file"
            :component="FormUpload"
            :default-value="magnet.geometry"
        />
        <Button type="submit" class="btn btn-primary">
          Save
        </Button>
      </Form>
    </Card>

    <Card class="mb-6">
      <template #header>
        <div class="flex items-center justify-between">
          <div>Parts</div>
          <Button
              v-if="magnet.status === 'in_study'"
              class="btn btn-primary btn-small"
              @click="addPartModalVisible = true"
          >
            Add a part
          </Button>
        </div>
      </template>

      <div class="table-responsive">
        <table>
          <thead class="bg-white">
            <tr>
              <th>Name</th>
              <th>Description</th>
              <th>Status</th>
              <th>Commissioned At</th>
              <th>Decommissioned At</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="magnetPart in magnet.magnet_parts" :key="magnetPart.id">
              <td>
                <router-link :to="{ name: 'part', params: { id: magnetPart.part.id } }" class="link">
                  {{ magnetPart.part.name }}
                </router-link>
              </td>
              <td>
                <template v-if="magnetPart.part.description">{{ magnetPart.part.description }}</template>
                <span v-else class="text-gray-500 italic">Not available</span>
              </td>
              <td>
                <StatusBadge :status="magnetPart.part.status"></StatusBadge>
              </td>
              <td>{{ magnetPart.commissioned_at | datetime }}</td>
              <td>{{ magnetPart.decommissioned_at | datetime }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </Card>

    <Card class="mb-6">
      <template #header>
        <div class="flex items-center justify-between">
          <div>Related Site</div>
          <Button
              v-if="['in_study', 'in_stock'].includes(magnet.status)"
              class="btn btn-primary btn-small"
              @click="attachToSiteModalVisible = true"
          >
            Attach to site
          </Button>
        </div>

      </template>

      <div class="table-responsive">
        <table>
          <thead class="bg-white">
            <tr>
              <th>Name</th>
              <th>Description</th>
              <th>Status</th>
              <th>Commissioned At</th>
              <th>Decommissioned At</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="siteMagnet in magnet.site_magnets" :key="siteMagnet.id">
              <td>
                <router-link :to="{ name: 'site', params: { id: siteMagnet.site.id } }" class="link">
                  {{ siteMagnet.site.name }}
                </router-link>
              </td>
              <td>
                <template v-if="siteMagnet.site.description">{{ siteMagnet.site.description }}</template>
                <span v-else class="text-gray-500 italic">Not available</span>
              </td>
              <td>
                <StatusBadge :status="siteMagnet.site.status"></StatusBadge>
              </td>
              <td>{{ siteMagnet.commissioned_at }}</td>
              <td>{{ siteMagnet.decommissioned_at }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </Card>

    <AddPartToMagnetModal
        :magnet-id="magnet.id"
        :visible="addPartModalVisible"
        @close="addPartModalVisible = false; fetch()"
    />
    <AttachMagnetToSiteModal
        :magnet-id="magnet.id"
        :visible="attachToSiteModalVisible"
        @close="attachToSiteModalVisible = false; fetch()"
    />
  </div>
  <Alert v-else-if="error" class="alert alert-danger" :error="error"/>
</template>

<script>
import * as Yup from 'yup'
import * as magnetService from '@/services/magnetService'
import Card from '@/components/Card'
import Form from "@/components/Form";
import FormField from "@/components/FormField";
import FormInput from "@/components/FormInput";
import FormSelect from "@/components/FormSelect";
import FormUpload from "@/components/FormUpload";
import Button from "@/components/Button";
import Alert from "@/components/Alert";
import AddPartToMagnetModal from "@/views/magnets/show/AddPartToMagnetModal";
import AttachMagnetToSiteModal from "@/views/magnets/show/AttachMagnetToSiteModal";
import StatusBadge from "@/components/StatusBadge";

export default {
  name: 'MagnetShow',
  components: {
    StatusBadge,
    AttachMagnetToSiteModal,
    AddPartToMagnetModal,
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
      magnet: null,
      addPartModalVisible: false,
      attachToSiteModalVisible: false,
    }
  },
  methods: {
    defunct() {
      return magnetService.defunct({ magnetId: this.magnet.id })
          .then(this.fetch)
          .catch((error) => {
            this.error = error
          })
    },
    submit(values, {setRootError}) {
      let payload = {
        id: this.magnet.id,
        name: values.name,
        description: values.description,
        design_office_reference: values.design_office_reference,
      }
      if (values.cao instanceof File) {
        payload.cao = values.cao
      }
      if (values.geometry instanceof File) {
        payload.geometry = values.geometry
      }

      return magnetService.update(payload)
          .then(this.fetch)
          .catch(setRootError)
    },
    validate() {
      return Yup.object().shape({
        name: Yup.string().required(),
      })
    },
    fetch() {
      return magnetService.find({id: this.$route.params.id})
          .then((magnet) => {
            this.magnet = magnet
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