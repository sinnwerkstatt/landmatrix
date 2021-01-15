<template>
  <div class="input-group">
    <!--    <label class="mr-sm-2 mb-0 sr-only" :for="formfield.name">-->
    <!--      {{ formfield.label }}-->
    <!--    </label>-->
    <input
      :id="formfield.name"
      v-model="val"
      :name="formfield.name"
      type="text"
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
    computed: {
      val: {
        get() {
          return this.value;
        },
        set(v) {
          this.$emit("input", v);
        },
      },
    },
  };
</script>
