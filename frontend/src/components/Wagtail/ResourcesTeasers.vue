<template>
  <div class="clamp-20-75p-56">
    <ArticleList :articles="value.articles" />
  </div>
</template>

<script>
  import ArticleList from "./ArticleList";

  export default {
    name: "ResourcesTeasers",
    components: { ArticleList },
    props: {
      value: { type: Object, required: true },
    },
  };
</script>
