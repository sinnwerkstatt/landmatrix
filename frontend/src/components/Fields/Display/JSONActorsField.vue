<template>
  <div class="jsonactors_field nowrap">
    <div v-for="val in vals">
      <span>{{ val.name }}</span>
      <span v-if="val.role" class="font-weight-light">
        ({{ mapChoices(val.role) }})
      </span>
    </div>
  </div>
</template>

<script lang="ts">
  import JSONFieldMixin from "../JSONFieldMixin";
  import Vue from "vue";

  export default Vue.extend({
    mixins: [JSONFieldMixin],
    data() {
      return {
        vals: this.value ? this.value : [{ name: null, role: null }],
      };
    },
  });
</script>
