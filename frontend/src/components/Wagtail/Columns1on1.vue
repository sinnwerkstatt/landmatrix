<template>
  <div class="container">
    <div class="row widget-columns-2">
      <div class="col-sm-6 col">
        <component
          v-for="x in value.left_column"
          :is="`wagtail-${x.type}`"
          :value="x.value"
          :key="x.id"
        ></component>
      </div>
      <div class="col-sm-6 col">
        <component
          v-for="x in value.right_column"
          :is="`wagtail-${x.type}`"
          :value="x.value"
          :key="x.id"
        />
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    props: ["value"],
  };
</script>
