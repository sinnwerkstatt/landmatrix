<template>
  <div>
    <div v-if="readonly">
      <span v-if="val">
        TRUE
      </span>
      <span v-else-if="val === false">
        FALSE
      </span>
      <span v-else>
        UNDEFINED
      </span>
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
