<template>
  <div class="streamfield">
    <div class="clamp-20-75p-56">
      <div v-for="block in content" :key="block.id">
        <component :is="`wagtail-${block.type}`" :value="block.value" />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
  import Vue from "vue";

  export default Vue.extend({
    name: "Streamfield",
    props: {
      content: { type: Array, default: () => [] },
    },
  });
</script>

<style scoped>
  h3 {
    text-align: center;
  }
  .streamfield {
    padding-top: 1.5em;
    padding-bottom: 0;
  }
</style>
