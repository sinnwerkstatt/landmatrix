<template>
  <div>
    <span v-if="value">
      {{ $t("Yes") }}
    </span>
    <span v-else-if="value === false">
      {{ $t("No") }}
    </span>
    <span v-else>
      NULL
    </span>
  </div>
</template>

<script>
  export default {
    props: {
      formfield: { type: Object, required: true },
      value: { type: Boolean, required: true },
      model: { type: String, required: true },
    },
  };
</script>
