<template>
  <div v-html="value"></div>
</template>

<script>
  export default {
    name: "WagtailParagraph",
    props: ["value"],
  };
</script>
