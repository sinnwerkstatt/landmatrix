<template>
  <div class="streamfield">
    <div class="container">
      <div v-for="block in content" :key="block.id">
        <component :is="`wagtail-${block.type}`" :value="block.value" />
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "Streamfield",
    props: {
      content: { type: Array, default: () => [] },
    },
  };
</script>

<style scoped>
  h3 {
    text-align: center;
  }
</style>
