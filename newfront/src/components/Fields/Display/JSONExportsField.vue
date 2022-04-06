<template>
  <div class="jsonexports_field whitespace-nowrap">
    <div v-for="val in vals" :class="{ 'font-weight-bold': val.current }">
      <span>{{ date_and_current(val) }}</span>
      <span v-if="val.choices">{{ mapChoices(val.choices) }}</span>
      <span v-if="val.area" class="mx-2">
        <i class="fas fa-circle-notch"></i> {{ val.area.toLocaleString("fr") }} ha
      </span>
      <span v-if="val.yield" class="mx-2">
        <i class="fas fa-weight-hanging"></i> {{ val.yield.toLocaleString("fr") }} tons
      </span>
      <span v-if="val.export" class="mx-2">
        <i class="fas fa-plane-departure"></i> {{ val.export.toLocaleString("fr") }} %
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
