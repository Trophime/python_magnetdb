<template>
  <div>
    <FormField v-for="magnet in magnets" :key="magnet.id" :label="`Current for ${magnet.name}`" :name="`i_${magnet.id}`"
      :component="FormInputWithUnit" type="number" :required="true" :unit-options="[
        {
          name: 'Ampère',
          value: 'A',
          symbol: 'A',
          default: true,
        },
        {
          name: 'Kilo Ampère',
          value: 'kA',
          symbol: 'kA',
          default: false,
        }
      ]" />
  </div>
</template>

<script>
import FormField from "@/components/FormField";
import FormInputWithUnit from "@/components/FormInputWithUnit";
import * as siteService from '@/services/siteService'
import * as magnetService from '@/services/magnetService'

export default {
  name: 'CurrentsField',
  inject: ['form'],
  components: { FormField },
  data: () => ({
    FormInputWithUnit,
    magnets: [],
  }),
  watch: {
    async 'form.values.resource'(resource) {
      console.log('CurrentsField')
      if (!resource) {
        return
      }

      console.log('CurrentsField (' + resource.value.type + ')')
      if (resource.value.type === 'site') {
        const site = await siteService.find({ id: resource.value.id })
        this.magnets = site.site_magnets
          .map((siteMagnet) => siteMagnet.magnet)
      } else if (resource.value.type === 'magnet') {
        const magnet = await magnetService.find({ id: resource.value.id })
        this.magnets = [magnet]
      }
    }
  },
}
</script>
