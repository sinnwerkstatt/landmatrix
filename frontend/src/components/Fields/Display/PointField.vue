<template>
  <div class="point_field">
    <div v-if="value.lat">Lat: {{ parseFloat(value.lat.toFixed(8)) }}</div>
    <div v-if="value.lng">Lng: {{ parseFloat(value.lng.toFixed(8)) }}</div>
  </div>
</template>

<script lang="ts">
  import type { PropType } from "vue";
  import type { FormField } from "$components/Fields/fields";
  import Vue from "vue";

  export default Vue.extend({
    props: {
      formfield: { type: Object as PropType<FormField>, required: true },
      value: { type: [Array, Object], required: true },
      model: { type: String, required: true },
    },
  });
</script>
