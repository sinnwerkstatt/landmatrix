<template>
  <div :class="['fullwidth', `fullwidth-${value.color}`]">
    <component
      :is="`wagtail-${x.type}`"
      v-for="x in value.content"
      :key="x.id"
      :value="x.value"
    />
  </div>
</template>

<script>
  export default {
    props: {
      value: { type: Object, required: true },
    },
  };
</script>

<style lang="scss" scoped>
  .fullwidth {
    padding: 1rem;
  }
  .fullwidth-darkgrey {
    background: #eee;
  }
</style>
