<template>
  <div class="nanoID_field">
    <router-link
      class="font-mono"
      :to="`${$route.hash.split('/')[0] || '#locations'}/${value}`"
    >
      {{ value }}
    </router-link>
  </div>
</template>

<script lang="ts">
  import type { FormField } from "$components/Fields/fields";
  import Vue from "vue";
  import type { PropType } from "vue";

  export default Vue.extend({
    props: {
      formfield: { type: Object as PropType<FormField>, required: true },
      value: { type: [String, Number], required: true },
      model: { type: String, required: true },
      targetBlank: { type: Boolean, default: false },
      objectVersion: { type: Number, default: null, required: false },
    },
  });
</script>
