<template>
  <div class="row mt-3">
    <div class="col-md-3 font-weight-bold">
      {{ formfield.label }}
    </div>
    <div class="col-md-9">
      <div v-if="readonly">
        <span v-for="val in vals">{{ val }}<br /></span>
      </div>
      <div v-else class="input-group">
        <div v-for="(key, val) in formfield.options">
          <label>
            <input type="checkbox" :value="key" />
            {{ val }}
          </label>
        </div>
        <br />
        <div v-for="val in vals"><input type="checkbox" />{{ val }}</div>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    props: ["formfield", "value", "readonly"],
    data() {
      return {
        vals: this.value,
      };
    },
    methods: {
      emitVal() {
        this.$emit("input", this.val);
      },
    },
  };
</script>
