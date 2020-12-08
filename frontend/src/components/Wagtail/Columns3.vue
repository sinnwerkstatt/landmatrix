<template>
  <div class="widget-columns-3 row">
    <div class="col-md-4">
      <component
        v-for="x in value.left_column"
        :is="`wagtail-${x.type}`"
        :value="x.value"
        :key="x.id"
      />
    </div>
    <div class="col-md-4">
      <component
        v-for="x in value.middle_column"
        :is="`wagtail-${x.type}`"
        :value="x.value"
        :key="x.id"
      />
    </div>
    <div class="col-md-4">
      <component
        v-for="x in value.right_column"
        :is="`wagtail-${x.type}`"
        :value="x.value"
        :key="x.id"
      />
    </div>
  </div>
</template>

<script>
  export default {
    props: ["value"],
  };
</script>
