<template>
  <div class="filter-collapse">
    <div @click="shown = !shown">
      {{ title }}
      <i class="fas" :class="[shown ? 'fa-chevron-up' : 'fa-chevron-down']"></i>
    </div>
    <div v-if="shown">
      <slot></slot>
    </div>
  </div>
</template>
<script>
  export default {
    props: ["title"],
    data() {
      return {
        shown: false,
      };
    },
  };
</script>

<style lang="scss">
  .filter-collapse {
    padding-top: 5px;
    padding-bottom: 5px;
    border-top: 1px solid #bbbbbb;
    border-bottom: 1px solid #bbbbbb;
  }
</style>
