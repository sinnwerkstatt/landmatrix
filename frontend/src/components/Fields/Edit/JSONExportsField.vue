<template>
  <div class="nowrap">
    <div v-for="val in vals" :class="{ 'font-weight-bold': val.current }">
      <span>{{ date_and_current(val) }}</span>
      <span v-if="val.choices">{{ mapChoices(val.choices) }}</span>
      <span v-if="val.area" class="mx-2">
        <i class="fas fa-circle-notch"></i> {{ val.area }} ha
      </span>
      <span v-if="val.yield" class="mx-2">
        <i class="fas fa-weight-hanging"></i> {{ val.yield }} tons
      </span>
      <span v-if="val.export" class="mx-2">
        <i class="fas fa-plane-departure"></i> {{ val.export }} %
      </span>
    </div>
  </div>
</template>

<script>
  import JSONField from "./JSONField";

  export default {
    mixins: [JSONField],
    data() {
      return {
        vals: this.value ? this.value : [{ date: null, value: null }],
      };
    },
  };
</script>
