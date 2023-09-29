<template>
  <div v-if="$route.query.code">
    <Alert v-if="error" :error="error" class="alert alert-danger" />
    <div v-else class="display-2 text-center">
      Loading...
    </div>
  </div>
  <div v-else-if="!error" class="space-y-6">
    <div class="display-1">
      Welcome to MagnetDB
    </div>

    <Card>
      <template #header>Introduction</template>
      <p>This is a demonstrator for MagnetDB. You can list, view, update and create objects by selecting appropriate object in the menu.</p>
      <p>An API also exists. To view the API docs and eventually test it, select the corresponding entry in the menubar.</p>
    </Card>

    <div class="grid grid-cols-4 gap-4">
      <Card>
        <template #header>Sites by status</template>
        <canvas ref="siteChart"></canvas>
      </Card>

      <Card>
        <template #header>Magnets by status</template>
        <canvas ref="magnetChart"></canvas>
      </Card>

      <div class="space-y-4">
        <Card>
          <template #header>Number of users</template>
          <div class="display-1">{{ users }}</div>
        </Card>

        <Card>
          <template #header>Number of records</template>
          <div class="display-1">{{ records }}</div>
        </Card>
      </div>
    </div>
  </div>
  <Alert v-else :error="error" class="alert alert-danger"></Alert>
</template>

<script>
import * as sessionService from '@/services/sessionService'
import Card from '@/components/Card'
import Alert from "@/components/Alert";
import * as homeService from "@/services/homeService";
import {Chart} from "chart.js";

export default {
  name: 'SignIn',
  components: {
    Alert,
    Card,
  },
  data() {
    return {
      error: null,
      users: null,
      records: null,
      siteChart: null,
      magnetChart: null,
    }
  },
  async mounted() {
    if (this.$route.query.code) {
      try {
        const res = await sessionService.create({
          code: this.$route.query.code,
          redirect_uri: `${window.location.origin}/sign_in`,
        })
        this.$store.commit('setToken', res.token)
        this.$router.push('/')
      } catch (error) {
        this.error = error
      }
      return
    }

    homeService.find()
        .then((res) => {
          this.siteChart = new Chart(this.$refs.siteChart, {
            type: 'pie',
            data: {
              labels: res.sites.map(v => v.status),
              datasets: [
                {
                  backgroundColor: [
                    'rgb(255, 99, 132)',
                    'rgb(54, 162, 235)',
                    'rgb(255, 205, 86)'
                  ],
                  data: res.sites.map(v => v.count),
                }
              ]
            },
          })
          this.magnetChart = new Chart(this.$refs.magnetChart, {
            type: 'pie',
            data: {
              labels: res.magnets.map(v => v.status),
              datasets: [
                {
                  backgroundColor: [
                    'rgb(255, 99, 132)',
                    'rgb(54, 162, 235)',
                    'rgb(255, 205, 86)'
                  ],
                  data: res.magnets.map(v => v.count),
                }
              ]
            },
          })
          this.users = res.users_count
          this.records = res.records_count
        })
        .catch((error) => {
          this.error = error
        })
  },
}
</script>
