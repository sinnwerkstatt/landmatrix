<template>
  <div class="nowrap">{{ val }}</div>
</template>

<script lang="ts">
  import dayjs from "dayjs";
  import Vue, { PropType } from "vue";
  import type { FormField } from "$components/Fields/fields";

  export default Vue.extend({
    name: "DateField",
    props: {
      formfield: { type: Object as PropType<FormField>, required: true },
      value: { type: [Date, String], required: true },
      model: { type: String, required: true },
    },
    computed: {
      val() {
        if (this.value) {
          // non-breaking hyphens would fix the stupid line break ("‑" vs "-")
          // return dayjs(this.value).format("YYYY‑MM‑DD"); 🤩️
          if (this.value.length === 4) return this.value;
          if (this.value.length === 7) return this.value;
          return dayjs(this.value).format("YYYY-MM-DD");
        } else {
          return "n/a";
        }
      },
    },
  });
</script>
