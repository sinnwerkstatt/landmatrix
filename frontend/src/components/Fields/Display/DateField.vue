<template>
  <div class="nowrap">{{ val }}</div>
</template>

<script>
  import dayjs from "dayjs";

  export default {
    name: "DateField",
    props: {
      formfield: { type: Object, required: true },
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
  };
</script>
