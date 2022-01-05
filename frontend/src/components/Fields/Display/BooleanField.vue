<template>
  <div class="boolean_field">
    <span v-if="value">
      {{ $t("Yes") }}
    </span>
    <span v-else-if="value === false">
      {{ $t("No") }}
    </span>
    <span v-else> NULL </span>
  </div>
</template>

<script lang="ts">
  import Vue from "vue";
  import type { PropType } from "vue";
  import type { FormField } from "$components/Fields/fields";

  export default Vue.extend({
    props: {
      formfield: { type: Object as PropType<FormField>, required: true },
      value: { type: Boolean, required: true },
      model: { type: String, required: true },
    },
  });
</script>
