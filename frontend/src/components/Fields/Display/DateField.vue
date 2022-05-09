<template>
  <div class="date_field whitespace-nowrap">{{ val }}</div>
</template>

<script lang="ts">
  import type { FormField } from "$components/Fields/fields";
  import dayjs from "dayjs";
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
        if (this.value) {
          // non-breaking hyphens would fix the stupid line break ("‑" vs "-")
          // return dayjs(this.value).format("YYYY‑MM‑DD"); 🤩️
          if (this.value.length === 4) return this.value;
          if (this.value.length === 7) return this.value;
          return dayjs(this.value).format("YYYY-MM-DD");
        }
        return "n/a";
      },
    },
  });
</script>
