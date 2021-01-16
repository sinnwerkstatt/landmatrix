<template>
  <div class="input-group">
    <!--    <label class="mr-sm-2 mb-0 sr-only" :for="formfield.name">-->
    <!--      {{ formfield.label }}-->
    <!--    </label>-->
    <input
      :id="formfield.name"
      v-model="int_val"
      :name="formfield.name"
      type="number"
      step="0.01"
      class="form-control"
      aria-describedby="validatedInputGroupPrepend"
      :required="formfield.required"
    />
    <div v-if="formfield.unit" class="input-group-append">
      <span id="validatedInputGroupPrepend" class="input-group-text">
        {{ formfield.unit }}
      </span>
    </div>
  </div>
</template>

<script>
  export default {
    props: {
      formfield: { type: Object, required: true },
      value: { type: Number, required: false, default: null },
      model: { type: String, required: true },
    },
    data() {
      return {
        int_val: this.value,
      };
    },
    watch: {
      int_val(v) {
        if (v.includes(".")) {
          let number = v.split(".");
          let decimals = number[1];
          decimals = decimals.length > 2 ? decimals.slice(0, 2) : decimals;
          this.int_val = `${number[0]}.${decimals}`;
        }
        this.$emit("input", +v);
      },
    },
  };
</script>
