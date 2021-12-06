<template>
  <div class="decimal_field nowrap">
    {{ val }}
    <span v-if="formfield.unit">{{ formfield.unit }}</span>
  </div>
</template>

<script lang="ts">
  import Vue, { PropType } from "vue";
  import type { FormField } from "$components/Fields/fields";

  export default Vue.extend({
    props: {
      formfield: { type: Object as PropType<FormField>, required: true },
      value: { type: Number, required: true },
      model: { type: String, required: true },
    },
    computed: {
      val(): string {
        if (this.formfield.choices) {
          return this.formfield.choices[this.value];
        }
        return this.value.toLocaleString("fr");
      },
    },
  });
</script>
