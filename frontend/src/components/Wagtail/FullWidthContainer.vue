<template>
  <div :class="['fullwidth', `fullwidth-${value.color}`]">
    <div class="container">
      <div class="row">
        <div class="col-md-12">
          <component
            v-for="x in value.content"
            :is="`wagtail-${x.type}`"
            :value="x.value"
            :key="x.id"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    props: ["value"],
  };
</script>

<style lang="scss">
  .fullwidth-darkgrey {
    background: #eee;
  }
</style>
