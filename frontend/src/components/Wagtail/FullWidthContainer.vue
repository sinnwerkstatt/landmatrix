<template>
  <div :class="['fullwidth', `fullwidth-${value.color}`]">
    <div class="container">
      <div class="row">
        <div class="col-md-12">
          <component
            :is="`wagtail-${x.type}`"
            v-for="x in value.content"
            :key="x.id"
            :value="x.value"
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
