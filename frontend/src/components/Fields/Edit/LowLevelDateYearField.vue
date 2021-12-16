<template>
  <div class="whitespace-nowrap input-group">
    <input
      ref="inputfield"
      v-model="val"
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
          this.valid_state = "";
          this.$refs.inputfield.setCustomValidity("");
          return;
        }
        v = v.replace("/", "-").replace(".", "-").replace(",", "-");

        let field_valid = dayjs(
          this.val,
          ["YYYY", "YYYY-M", "YYYY-M-D", "YYYY-MM", "YYYY-MM-D", "YYYY-MM-DD"],
          true
        ).isValid();

        if (field_valid) {
          this.valid_state = "is-valid";
          this.$refs.inputfield.setCustomValidity("");
        } else {
          this.valid_state = "is-invalid";
          this.$refs.inputfield.setCustomValidity(
            "Invalid format. Use YYYY, YYYY-MM or YYYY-MM-DD"
          );
        }

        this.$emit("input", v);
      },
    },
  };
</script>
