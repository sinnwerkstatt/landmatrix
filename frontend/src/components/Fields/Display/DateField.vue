<template>
  <div class="date_field whitespace-nowrap">{{ val }}</div>
</template>

<script lang="ts">
  import type { FormField } from "$components/Fields/fields";
  import Vue from "vue";
  import type { PropType } from "vue";

  export default Vue.extend({
    name: "DateField",
    props: {
      formfield: { type: Object as PropType<FormField>, required: true },
      value: { type: [Date, String], required: true },
      model: { type: String, required: true },
    },
    computed: {
      val(): string {
        // non-breaking hyphens would fix the stupid line break ("‑" vs "-")
        // return dayjs(this.value).format("YYYY‑MM‑DD"); 🤩️
        return this.value ?? "n/a";
      },
    },
  });
</script>
