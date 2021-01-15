<template>
  <div class="nowrap">
    <div v-for="val in vals" :class="{ 'font-weight-bold': val.current }">
      <span>{{ date_and_current(val) }}</span>
      <span v-if="val.choices">{{ mapChoices(val.choices) }}</span>
      <span v-if="val.area">({{ val.area }} ha)</span>
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
