<template>
  <div>
    <div v-for="block in content">
      <component :is="`wagtail-${block.type}`" :value="block.value" />
    </div>
  </div>
</template>

<script>
  export default {
    name: "Streamfield",
    props: ["content"],
  };
</script>

<style scoped></style>
