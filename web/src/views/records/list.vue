<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <div class="display-1">
        Records from MagnetDB
      </div>
      <router-link class="btn btn-success" :to="{ name: 'new_record' }">
        New record
      </router-link>
    </div>

    <Card>
      <DataTable
        :headers="headers" @fetch="fetch" config-persistence-key="record-list"
        @item-selected="$router.push({ name: 'record', params: { id: $event.id } })"
      >
        <template v-slot:item.name="{ item }">
          {{ item.name }}
        </template>
        <template v-slot:item.description="{ item }">
          <template v-if="item.description">{{ item.description }}</template>
          <span v-else class="text-gray-500 italic">Not available</span>
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
import * as recordService from '@/services/recordService'
import Card from '@/components/Card'
import DataTable from "@/components/DataTable";

export default {
  name: 'RecordList',
  components: {
    Card,
    DataTable,
  },
  data() {
    return {
      headers: [
        {
          key: 'name',
          name: 'Name',
          default: true,
          sortable: true,
        },
        {
          key: 'description',
          name: 'Description',
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
      return recordService.list({ query, page, perPage, sortBy, sortDesc }).then((res) => ({
        currentPage: res.current_page,
        lastPage: res.last_page,
        items: res.items,
        query,
        perPage,
        sortBy,
        sortDesc: sortDesc === null ? true : sortDesc,
      }))
    },
  },
}
</script>
