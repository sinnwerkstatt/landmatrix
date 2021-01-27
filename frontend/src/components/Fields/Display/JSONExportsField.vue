<template>
  <div class="nowrap">
    <div v-for="val in vals" :class="{ 'font-weight-bold': val.current }">
      <span>{{ date_and_current(val) }}</span>
      <span v-if="val.choices">{{ mapChoices(val.choices) }}</span>
      <span v-if="val.area" class="mx-2">
        <i class="fas fa-circle-notch"></i> {{ val.area.toLocaleString() }} ha
      </span>
      <span v-if="val.yield" class="mx-2">
        <i class="fas fa-weight-hanging"></i> {{ val.yield.toLocaleString() }} tons
      </span>
      <span v-if="val.export" class="mx-2">
        <i class="fas fa-plane-departure"></i> {{ val.export.toLocaleString() }} %
      </span>
    </div>
  </div>
</template>

<script>
  import JSONFieldMixin from "../JSONFieldMixin";

  export default {
    mixins: [JSONFieldMixin],
    data() {
      return {
        vals: this.value ? this.value : [{ date: null, value: null }],
      };
    },
  };
</script>
