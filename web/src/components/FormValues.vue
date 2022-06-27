<script>
export default {
  name: 'FormValues',
  inject: ['form'],
  render() {
    return this.$scopedSlots.default({ values: this.form.values })
  },
}
</script>
