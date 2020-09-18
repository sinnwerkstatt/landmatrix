<template>
  <div class="container">
    <div v-html="value"></div>
  </div>
</template>

<script>
  export default {
    props: ["value"],
  };
</script>
