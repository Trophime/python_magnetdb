<template>
  <div>
    <div ref="slider" />
    <div class="flex items-center justify-center mt-2 space-x-2">
      <template v-if="isArray">
        <FormInput
          class="border border-gray-200 py-0.5 px-2 text-center"
          :value="value[0]"
          style="width: 25%"
          @value="handleChange([$event, value[1]])"
        />
        <div>-</div>
        <FormInput
          class="border border-gray-200 py-0.5 px-2 text-center"
          :value="value[1]"
          style="width: 25%"
          @value="handleChange([value[0], $event])"
        />
      </template>
      <FormInput
        v-else
        class="border border-gray-200 py-0.5 px-2 text-center"
        :value="value"
        style="width: 25%"
        @value="handleChange([$event])"
      />
    </div>
  </div>
</template>

<script>
import noUiSlider from 'nouislider'
import 'nouislider/dist/nouislider.css';
import FormInput from "@/components/FormInput.vue";

export default {
  name: 'FormSlider',
  components: {FormInput},
  props: ['min', 'max', 'value', 'step'],
  data: () => ({
    slider: null,
  }),
  computed: {
    isArray() {
      return this.value instanceof Array
    },
    displayableValue() {
      return this.isArray ? this.value.join(' - ') : this.value
    },
  },
  methods: {
    handleChange(values) {
      this.slider.set(values)
      const range = values.map((event) => parseFloat(event))
      if (range.every((value) => !Number.isNaN(value))) {
        this.$emit('value', range.length === 1 ? range[0] : range)
      }
    },
  },
  mounted() {
    this.slider = noUiSlider.create(this.$refs.slider, {
      start: this.value,
      connect: true,
      behaviour: 'drag',
      step: this.step,
      range: {
        'min': this.min,
        'max': this.max,
      }
    })
    this.slider.on('change', (event) => {
      const range = event.map((event) => parseFloat(event))
      this.$emit('value', range.length === 1 ? range[0] : range)
    })
  },
  destroyed() {
    this.slider.destroy?.()
  }
}
</script>

<style>
.noUi-horizontal .noUi-handle {
  width: 20px;
  height: 20px;
  right: -17px;
  top: -3px;
  border-radius: 100%;
}

.noUi-handle:before, .noUi-handle:after {
  display: none;
}
</style>