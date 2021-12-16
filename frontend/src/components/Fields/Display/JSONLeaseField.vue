<template>
  <div class="jsonlease_field whitespace-nowrap">
    <div v-for="val in vals" :class="{ 'font-weight-bold': val.current }">
      <span>{{ date_and_current(val) }}</span>
      <span v-if="val.area" class="mx-2">
        <i class="fas fa-circle-notch"></i> {{ val.area.toLocaleString("fr") }} ha
      </span>
      <span v-if="val.farmers" class="mx-2">
        <i class="fas fa-tractor"></i> {{ val.farmers.toLocaleString("fr") }}
      </span>
      <span v-if="val.households" class="mx-2">
        <i class="fas fa-home"></i> {{ val.households.toLocaleString("fr") }}
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
