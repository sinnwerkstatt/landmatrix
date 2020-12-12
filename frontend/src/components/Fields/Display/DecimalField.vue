<template>
  <div>
    {{ value.toLocaleString() }}
  </div>
</template>

<script>
  export default {
    props: ["formfield", "value", "model"],
  };
</script>
