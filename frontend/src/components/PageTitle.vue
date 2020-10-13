<template>
  <div v-if="title" class="container">
    <div class="row">
      <div class="col-md-12">
        <h1>
          <span v-html="title"></span>
        </h1>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    props: ["title"],
  };
</script>
