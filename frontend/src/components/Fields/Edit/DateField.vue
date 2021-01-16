<template>
  <div>
    <v-date-picker
      v-model="val"
      :masks="{ input: 'YYYY-MM-DD' }"
      :max-date="new Date()"
      :input-props="{ style: 'width: 100%' }"
    />
  </div>
</template>

<script>
  import dayjs from "dayjs";

  export default {
    name: "DateField",
    props: {
      formfield: { type: Object, required: true },
      value: { type: [Date, String], required: false, default: null },
      model: { type: String, required: true },
    },
    computed: {
      val: {
        get() {
          return this.value ? dayjs(this.value).toDate() : null;
        },
        set(v) {
          this.$emit("input", dayjs(v).format("YYYY-MM-DD"));
        },
      },
    },
  };
</script>
