<template>
  <Card v-show="display">
    <template #header>
      Magnetic field of the last created magnet
    </template>

    <canvas ref="chart"></canvas>
  </Card>
</template>

<script>
import * as magnetService from "@/services/magnetService";
import Card from "@/components/Card";
import * as visualisationService from "@/services/visualisationService";
import {Chart} from "chart.js";

export default {
  name: 'LastMagnetFieldCard',
  components: {Card},
  data() {
    return {
      display: false,
    }
  },
  async mounted() {
    try {
      const magnets = await magnetService.list({ page: 1, perPage: 1, sortBy: 'created_at', sortDesc: true })
      if (magnets.items.length === 1) {
        const { results: data } = await visualisationService.bmap({
          resource_id: magnets.items[0].id,
          resource_type: 'magnet',
        })
        this.chart = new Chart(this.$refs.chart, {
          type: 'line',
          data: {
            labels: data.x,
            datasets: [
              {
                label: `Y`,
                backgroundColor: '#FF0000',
                borderColor: '#FF0000',
                data: data.y,
              },
              {
                label: `Y`,
                backgroundColor: '#00FF00',
                borderColor: '#00FF00',
                data: data.ymax,
              },
            ],
          },
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
                  text: data.yaxis
                },
              },
            },
          },
        })
        this.display = true
      }
    } catch (error) {
      console.error(error)
    }
  },
}
</script>
