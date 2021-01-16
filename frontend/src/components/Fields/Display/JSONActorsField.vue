<template>
  <div class="nowrap">
    <div v-for="val in vals">
      <span>{{ val.name }}</span>
      <span v-if="val.role" class="font-weight-light">
        ({{ mapChoices(val.role) }})
      </span>
    </div>
  </div>
</template>

<script>
  import JSONFieldMixin from "../JSONFieldMixin";

  export default {
    mixins: [JSONFieldMixin],
    data() {
      return {
        vals: this.value ? this.value : [{ name: null, role: null }],
      };
    },
  };
</script>
