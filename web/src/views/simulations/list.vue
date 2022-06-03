<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <div class="display-1">
        Simulations from MagnetDB
      </div>
      <router-link class="btn btn-success" :to="{ name: 'new_simulation' }">
        New simulation
      </router-link>
    </div>

    <Card>
      <DataTable
        :headers="headers" @fetch="fetch" config-persistence-key="simulation-list"
        @item-selected="$router.push({ name: 'simulation', params: { id: $event.id } })"
      >
        <template v-slot:item.resource="{ item }">
          {{ item.resource.name }} <span class="text-gray-500">({{ item.resource_type }})</span>
        </template>
        <template v-slot:item.status="{ item }">
          <StatusBadge :status="item.status"></StatusBadge>
        </template>
        <template v-slot:item.setup_status="{ item }">
          <StatusBadge :status="item.setup_status"></StatusBadge>
        </template>
        <template v-slot:item.created_at="{ item }">
          {{ item.created_at | datetime }}
        </template>
        <template v-slot:item.updated_at="{ item }">
          {{ item.updated_at | datetime }}
        </template>
      </DataTable>
    </Card>
  </div>
</template>

<script>
import * as simulationService from '@/services/simulationService'
import Card from '@/components/Card'
import DataTable from "@/components/DataTable";
import StatusBadge from "@/components/StatusBadge";

export default {
  name: 'SimulationList',
  components: {
    StatusBadge,
    Card,
    DataTable,
  },
  data() {
    return {
      headers: [
        {
          key: 'resource',
          name: 'Resource',
          default: true,
        },
        {
          key: 'status',
          name: 'Status',
          default: true,
        },
        {
          key: 'method',
          name: 'Method',
        },
        {
          key: 'model',
          name: 'Model',
        },
        {
          key: 'geometry',
          name: 'Geometry',
        },
        {
          key: 'cooling',
          name: 'Cooling',
        },
        {
          key: 'setup_status',
          name: 'Setup Status',
          default: true,
        },
        {
          key: 'created_at',
          name: 'Created At',
          default: true,
          sortable: true,
        },
        {
          key: 'updated_at',
          name: 'Updated At',
          sortable: true,
        },
      ]
    }
  },
  methods: {
    fetch({ query, page, perPage, sortBy, sortDesc }) {
      return simulationService.list({ query, page, perPage, sortBy, sortDesc }).then((res) => ({
        currentPage: res.current_page,
        lastPage: res.last_page,
        items: res.items,
        perPage,
        query,
        sortBy,
        sortDesc: sortDesc === null ? true : sortDesc,
      }))
    },
  },
}
</script>
