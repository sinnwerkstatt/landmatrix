<template>
  <span class="status_field">{{ display_status }}</span>
</template>

<script lang="ts">
  import { combined_status_fn } from "$utils/choices";
  import Vue from "vue";
  import type { PropType } from "vue";

  export default Vue.extend({
    props: {
      formfield: { type: Object, required: true },
      value: { type: Array as PropType<number[]>, required: true },
      model: { type: String, required: true },
    },
    computed: {
      display_status() {
        return this.$t(combined_status_fn(this.value[0], this.value[1], true));
      },
    },
  });
</script>
