<template>
  <div class="widget-columns-3">
    <div>
      <component
        :is="`wagtail-${x.type}`"
        v-for="x in value.left_column"
        :key="x.id"
        :value="x.value"
      />
    </div>
    <div>
      <component
        :is="`wagtail-${x.type}`"
        v-for="x in value.middle_column"
        :key="x.id"
        :value="x.value"
      />
    </div>
    <div>
      <component
        :is="`wagtail-${x.type}`"
        v-for="x in value.right_column"
        :key="x.id"
        :value="x.value"
      />
    </div>
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
  .widget-columns-3 {
    display: flex;
    flex-flow: column;
    gap: 1rem;
    margin-bottom: 2rem;

    > * {
      flex-basis: 100%;
    }

    @media screen and (min-width: 45rem) {
      flex-flow: row;
    }
  }
</style>
