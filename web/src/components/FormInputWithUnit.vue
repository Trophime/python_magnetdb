<template>
  <div class="form-input-with-unit-container">
    <input
        v-bind="$attrs"
        class="form-input"
        :class="{ 'form-input-error': hasError }"
        type="number"
        :value="value"
        @input="onInput"
    />
    <div class="unit-name">
      {{defaultUnit.symbol}}
    </div>
    <button ref="button" type="button" class="more-button btn btn-default" @click="toggleConverter = !toggleConverter">
      <DotsHorizontalIcon class="w-5 h-5"/>
    </button>
    <form v-if="toggleConverter" ref="dialog" class="conversion-dialog" @submit.prevent="convert">
      <FormInput type="number" :value="valueWithCustomUnit" @value="valueWithCustomUnit = $event" />
      <FormSelect :value="unit" :options="unitOptions" @value="changeUnit" />
      <Button type="submit" class="btn btn-primary btn-block" @click="convert">
        Convert
      </Button>
    </form>
  </div>
</template>

<script>
import { unit } from 'mathjs'
import {DotsHorizontalIcon} from '@vue-hero-icons/outline'
import FormInput from "@/components/FormInput";
import FormSelect from "@/components/FormSelect";
import Button from "@/components/Button";

window.mathUnit = unit

export default {
  name: 'FormInputWithUnit',
  inheritAttrs: false,
  props: ['value', 'unitOptions', 'hasError'],
  inject: ['form'],
  data() {
    return {
      toggleConverter: false,
      valueWithCustomUnit: null,
      defaultUnit: null,
      unit: null,
    }
  },
  components: {
    Button,
    FormSelect,
    FormInput,
    DotsHorizontalIcon,
  },
  watch: {
    toggleConverter() {
      this.valueWithCustomUnit = this.value
      this.unit = this.defaultUnit
    },
  },
  methods: {
    onInput(event) {
      this.$emit('value', event.target.value)
    },
    changeUnit(newUnit) {
      if (this.valueWithCustomUnit) {
        this.valueWithCustomUnit = unit(this.valueWithCustomUnit, this.unit.value).to(newUnit.value).toNumber()
      }
      this.unit = newUnit
    },
    convert() {
      if (this.valueWithCustomUnit) {
        const value = unit(this.valueWithCustomUnit, this.unit.value).to(this.defaultUnit.value).value
        this.$emit('value', value)
      }
      this.toggleConverter = false
    },
    watchClick(event) {
      if (this.toggleConverter && !(event.path.includes(this.$refs.dialog) || event.path.includes(this.$refs.button))) {
        this.toggleConverter = false
      }
    }
  },
  created() {
    const defaultUnit = this.unitOptions.find((opt) => opt.default)
    this.defaultUnit = defaultUnit
    this.unit = defaultUnit
  },
  mounted() {
    window.addEventListener('click', this.watchClick)
  },
  beforeDestroy() {
    window.removeEventListener('click', this.watchClick)
  },
}
</script>

<style scoped>
.form-input-with-unit-container {
  @apply z-0 relative flex items-center block w-full shadow-sm sm:text-sm border border-gray-300 rounded-md
  focus:ring-blue-500 focus:border-blue-500;
}

.form-input-with-unit-container > .more-button {
  @apply px-1 h-6 mr-2;
}

.form-input-with-unit-container > .unit-name {
  @apply text-gray-500 font-medium ml-2 mr-4;
}

.form-input-with-unit-container > .form-input {
  @apply block border-none w-full sm:text-sm rounded-l-md focus:ring-0;
}

.form-input:disabled {
  @apply bg-gray-100 cursor-not-allowed;
}

.form-input-error {
  @apply ring-1 border-red-500 ring-red-500 !important;
}

.conversion-dialog {
  @apply right-2 absolute bg-white p-4 border border-gray-300 rounded-md shadow-md space-y-2;
  z-index: 2000000;
  height: 170px;
  width: 340px;
  top: -175px;
}
</style>
