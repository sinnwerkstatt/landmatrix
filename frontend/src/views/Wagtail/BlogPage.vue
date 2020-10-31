<template>
  <div>
    <PageTitle v-if="article" :title="article.title"></PageTitle>

    <div class="container" v-if="article">
      <div class="meta mb-3">
        <div class="date d-inline-block mr-4">
          <i class="far fa-calendar-alt"></i> {{ article.date }}
        </div>
        <div v-if="article.tags.length > 0" class="tags d-inline-block">
          <router-link
            v-for="tag in article.tags"
            :to="`/stay-informed/?tag=${tag.slug}`"
          >
            <i class="fas fa-tags"></i> {{ tag.name }}
          </router-link>
        </div>
      </div>
      <div class="blog-body" v-html="article.body" />
    </div>
  </div>
</template>

<script>
  import gql from "graphql-tag";
  import PageTitle from "../../components/PageTitle";

  export default {
    components: { PageTitle },
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
              tags {
                slug
                name
              }
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
