<template>
  <div class="widget-columns-2 row">
    <div class="col-sm-6 col">
      <component
        :is="`wagtail-${x.type}`"
        v-for="x in value.left_column"
        :key="x.id"
        :value="x.value"
      ></component>
    </div>
    <div class="col-sm-6 col">
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
