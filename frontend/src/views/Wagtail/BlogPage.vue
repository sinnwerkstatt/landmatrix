<template>
  <div class="container" v-if="article">
    <div class="meta date">
      {{ article.date }}
    </div>
    <div v-html="article.body" />
    <div class="meta">
      <div v-if="article.tags.length > 0" class="tags">
        Tags:

        <a v-for="tag in article.tags" :href="tag.slug">{{ tag.name }}</a>
      </div>
    </div>
  </div>
</template>

<script>
  import gql from "graphql-tag";

  export default {
    data() {
      return {
        article: null,
      };
    },
    apollo: {
      article: {
        query: gql`
          query Article($id: Int!) {
            blogpage(id: $id) {
              id
              title
              body
              date
              tags { slug name }
            }
          }
        `,
        update: (data) => data.blogpage,
        variables() {
          return {
            id: this.$store.state.page.wagtailPage.id,
          };
        },
      },
    },
  };
</script>

<style lang="scss"></style>
