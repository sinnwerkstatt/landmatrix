<template>
  <div>{{ val }}</div>
</template>

<script>
  import dayjs from "dayjs";

  export default {
    name: "DateField",
    props: ["formfield", "value"],
    computed: {
      val() {
        if (this.value) {
          return dayjs(this.value).format("YYYY-MM-DD");
        } else {
          return "n/a";
        }
      },
    },
  };
</script>
