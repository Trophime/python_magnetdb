<template>
  <div>
    <div ref="slider" />
    <div class="text-center text-gray-700 text-sm font-semibold mt-1">
      {{displayableValue}}
    </div>
  </div>
</template>

<script>
import noUiSlider from 'nouislider'
import 'nouislider/dist/nouislider.css';

export default {
  name: 'FormSlider',
  props: ['min', 'max', 'value'],
  data: () => ({
    slider: null,
  }),
  computed: {
    displayableValue() {
      return this.value?.join?.(' - ') ?? this.value
    },
  },
  mounted() {
    this.slider = noUiSlider.create(this.$refs.slider, {
      start: this.value,
      connect: true,
      behaviour: 'drag',
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