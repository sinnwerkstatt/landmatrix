<template>
  <div class="widget-columns-3 row">
    <div class="col-md-4">
      <component
        :is="`wagtail-${x.type}`"
        v-for="x in value.left_column"
        :key="x.id"
        :value="x.value"
      />
    </div>
    <div class="col-md-4">
      <component
        :is="`wagtail-${x.type}`"
        v-for="x in value.middle_column"
        :key="x.id"
        :value="x.value"
      />
    </div>
    <div class="col-md-4">
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
