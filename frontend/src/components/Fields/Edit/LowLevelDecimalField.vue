<template>
  <div class="nowrap input-group">
    <input
      v-model="val"
      type="number"
      class="form-control"
      :placeholder="placeholder"
      :required="required"
      :min="minValue"
      :max="maxValue"
      :step="step"
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
      unit: { type: String, required: false, default: "" },
      required: { type: Boolean, default: false },
      value: { type: Number, required: false, default: null },
      maxValue: { type: Number, required: false, default: null },
      minValue: { type: Number, required: false, default: null },
      decimals: { type: Number, default: 2 },
    },
    data() {
      return {
        val: JSON.parse(JSON.stringify(this.value)),
      };
    },
    // Nice to have: on up/down-arrow: change the number where the cursor is on..
    // methods: {
    //   updowndings(e) {
    //     if (["ArrowUp", "ArrowDown"].includes(e.key)) {
    //       e.preventDefault();
    //       console.log(e.key);
    //       console.log(e.target.selectionStart);
    //       console.log(e.target);
    //     }
    //   },
    // },
    computed: {
      placeholder() {
        if (this.minValue !== null && this.maxValue !== null) {
          return `${this.minValue} – ${this.maxValue}`;
        }
        if (this.step === 1) return "";
        return "100.23";
      },
      step() {
        return 1 / 10 ** this.decimals;
      },
    },
    watch: {
      value(newValue) {
        this.val = JSON.parse(JSON.stringify(newValue));
      },
      val(v) {
        if (!v && v !== 0) {
          this.$emit("input", null);
          return;
        }
        if (this.maxValue && v > this.maxValue) this.val = this.maxValue;
        if (this.minValue && v < this.minValue) this.val = this.minValue;

        let v_str = v.toString();
        if (v_str.includes(".")) {
          let number = v_str.split(".");
          let decs = number[1];
          decs = decs.length > this.decimals ? decs.slice(0, this.decimals) : decs;
          v_str = `${number[0]}.${decs}`;
          this.val = v_str;
        }
        this.$emit("input", +v);
      },
    },
  };
</script>
