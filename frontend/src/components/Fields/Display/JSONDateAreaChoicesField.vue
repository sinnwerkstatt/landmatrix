<template>
  <div class="jsondateareachoices_field">
    <div v-for="val in vals" :class="{ 'font-weight-bold': val.current }">
      <span>{{ date_and_current(val) }} </span>
      <span v-if="val.choices">{{ mapChoices(val.choices) }}</span>
      <span v-if="val.area">
        (<i class="fas fa-circle-notch"></i> {{ val.area.toLocaleString("fr") }} ha)
      </span>
    </div>
  </div>
</template>

<script>
  import Vue from "vue";
  import JSONFieldMixin from "../JSONFieldMixin";

  export default Vue.extend({
    mixins: [JSONFieldMixin],
    data() {
      return {
        vals: this.value ? this.value : [{ date: null, value: null }],
      };
    },
  });
</script>
