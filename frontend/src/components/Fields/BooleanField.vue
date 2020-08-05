<template>
  <div class="row">
    <div class="col-md-3 font-weight-bold">
      {{ formfield.label }}
    </div>
    <div class="col-md-9">
      <div v-if="readonly">
        <span v-if="val">
          Yes
        </span>
        <span v-else-if="val === false">
          No
        </span>
        <span v-else>
          NULL
        </span>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    props: ["formfield", "value", "readonly"],
    data() {
      return {
        val: this.value,
      };
    },
    methods: {
      emitVal() {
        this.$emit("input", this.val);
      },
    },
  };
</script>
