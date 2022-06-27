<template>
  <div class="space-y-4">
    <Alert :error="error" />

    <div v-if="resource" class="display-1">
      {{resource.name}}
    </div>

    <Card v-if="params">
      <Form :initial-values="params" @change="handleChanges">
        <div class="flex items-center space-x-4">
          <div class="w-1/3">
            <FormField
                v-if="allowedCurrents.includes('i_h')"
                label="I h"
                name="i_h"
                :component="FormSlider"
                :min="0"
                :max="35000"
            />
          </div>
          <div class="w-1/3">
            <FormField
                v-if="allowedCurrents.includes('i_b')"
                label="I b"
                name="i_b"
                :component="FormSlider"
                :min="0"
                :max="35000"
            />
          </div>
          <div class="w-1/3">
            <FormField
                v-if="allowedCurrents.includes('i_s')"
                label="I s"
                name="i_s"
                :component="FormSlider"
                :min="0"
                :max="37000"
            />
          </div>
        </div>
        <div class="flex items-center space-x-4">
          <div class="w-1/3">
            <FormField
                label="N"
                name="n"
                :component="FormSlider"
                :min="50"
                :max="1000"
                :step="1"
            />
          </div>
          <div class="w-1/3">
            <FormField
                label="Z"
                name="z"
                :component="FormSlider"
                :min="-0.2"
                :max="0.2"
            />
          </div>
        </div>
        <div class="flex items-center space-x-4">
          <div class="w-1/3">
            <FormField
                label="Pkey"
                name="pkey"
                :component="FormSelect"
                :options="['A', 'Br', 'Bz', 'B']"
            />
          </div>
        </div>
      </Form>
    </Card>
    <Card>
      <canvas ref="chart"></canvas>
    </Card>
  </div>
</template>

<script>
import * as visualisationService from '@/services/visualisationService'
import {Chart} from "chart.js";
import Card from "@/components/Card";
import FormSlider from "@/components/FormSlider";
import Form from "@/components/Form";
import FormField from "@/components/FormField";
import FormInput from "@/components/FormInput";
import FormSelect from "@/components/FormSelect";
import Alert from "@/components/Alert";
import * as siteService from "@/services/siteService";
import * as magnetService from "@/services/magnetService";

export default {
  name: 'StressMapVisualisation',
  components: {
    Alert,
    FormField,
    Form,
    Card
  },
  data() {
    return {
      FormSlider,
      FormInput,
      FormSelect,
      params: null,
      chart: null,
      error: null,
      resource: null,
      allowedCurrents: [],
    }
  },
  methods: {
    handleChanges(values) {
      return this.fetch(values)
    },
    async fetch(values) {
      try {
        const { results: data, params, allowed_currents: allowedCurrents } = await visualisationService.stressMap({
          ...values,
          resource_id: this.$route.query.resource_id,
          resource_type: this.$route.query.resource_type,
        })
        this.params = params
        this.allowedCurrents = allowedCurrents
        if (!this.chart) {
          this.chart = new Chart(this.$refs.chart, {
            type: 'bar',
            data: {},
            options: {
              scales: {
                x: {
                  title: {
                    display: true,
                    text: '[m]'
                  },
                },
                y: {
                  title: {
                    display: true,
                    text: ''
                  },
                },
              },
              plugins: {
                zoom: {
                  zoom: {
                    drag: {
                      enabled: true
                    },
                    mode: 'xy',
                  },
                }
              },
            },
          })
        }

        this.chart.options.scales.y.title.text = data.yaxis
        this.chart.data = {
          labels: data.x,
          datasets: [
            {
              label: `I`,
              backgroundColor: '#FF0000',
              borderColor: '#FF0000',
              data: data.y,
            },
            {
              label: `I nominal`,
              backgroundColor: '#00FF00',
              borderColor: '#00FF00',
              data: data.ymax,
            },
          ],
        }
        this.chart.update()
        this.$router.replace({
          name: this.$route.name,
          query: {
            ...this.$route.query,
            ...params,
          },
        }).catch(() => {})
      } catch (error) {
        this.error = error
      }
    },
  },
  async mounted() {
    await Promise.all([
      this.fetch(this.$route.query),
      (async () => {
        const resourceId = this.$route.query.resource_id
        switch (this.$route.query.resource_type) {
          case 'site':
            this.resource = await siteService.find({ id: resourceId })
            break
          case 'magnet':
            this.resource = await magnetService.find({ id: resourceId })
            break
        }
      })(),
    ])
  }
}
</script>
