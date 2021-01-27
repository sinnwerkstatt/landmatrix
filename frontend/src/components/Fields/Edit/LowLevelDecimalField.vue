<template>
  <div class="nowrap input-group">
    <input
      v-model="val"
      type="number"
      step="0.01"
      class="form-control"
      placeholder="100.23"
      :required="required"
      :max="maxValue"
    />
    <div v-if="unit" class="input-group-append">
      <span class="input-group-text">
        {{ unit }}
      </span>
    </div>
  </div>
</template>

<script>
  export default {
    name: "LowLevelDecimalField",
    props: {
      label: { type: String, required: false, default: "" },
      unit: { type: String, required: false, default: "" },
      required: { type: Boolean, default: false },
      value: { type: Number, required: false, default: null },
      maxValue: { type: Number, required: false, default: null },
    },
    data() {
      return {
        val: this.value,
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
        if (this.maxValue && v > this.maxValue) {
          this.val = this.maxValue;
        }
        let v_str = v.toString();
        if (v_str.includes(".")) {
          let number = v_str.split(".");
          let decimals = number[1];
          decimals = decimals.length > 2 ? decimals.slice(0, 2) : decimals;
          v_str = `${number[0]}.${decimals}`;
          this.val = v_str;
        }
        this.$emit("input", +v);
      },
    },
  };
</script>
