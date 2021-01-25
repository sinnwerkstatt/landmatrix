<template>
  <div class="nowrap input-group">
    <label class="sr-only" :for="name">{{ label }}</label>
    <input
      :id="name"
      v-model="val"
      :name="name"
      type="text"
      class="form-control"
      :class="valid_state"
      placeholder="YYYY-MM-DD"
      :required="required"
    />
  </div>
</template>

<script>
  import dayjs from "dayjs";
  import customParseFormat from "dayjs/plugin/customParseFormat";

  dayjs.extend(customParseFormat);

  export default {
    name: "LowLevelDateYearField",
    props: {
      name: { type: String, required: true },
      label: { type: String, required: false, default: "" },
      unit: { type: String, required: false, default: "" },
      required: { type: Boolean, default: false },
      value: { type: [String, Date], required: false, default: null },
    },
    data() {
      return {
        val: this.value,
        valid_state: null,
      };
    },
    watch: {
      value(newValue) {
        this.val = newValue;
      },
      val(v) {
        if (!v) {
          this.$emit("input", null);
          return;
        }
        v = v.replace("/", "-");

        this.valid_state = dayjs(
          this.val,
          ["YYYY", "YYYY-M", "YYYY-M-D", "YYYY-MM", "YYYY-MM-D", "YYYY-MM-DD"],
          true
        ).isValid()
          ? "is-valid"
          : "is-invalid";

        this.$emit("input", v);
      },
    },
  };
</script>
