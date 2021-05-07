<template>
  <div>
    <PageTitle v-if="blogpage" :title="blogpage.title" />

    <div v-if="blogpage" class="container">
      <div class="meta mb-3">
        <div class="date d-inline-block mr-4">
          <i class="far fa-calendar-alt" /> {{ blogpage.date }}
        </div>
        <div v-if="blogpage.tags.length > 0" class="tags d-inline-block">
          <router-link
            v-for="tag in blogpage.tags"
            :key="tag.slug"
            :to="`/stay-informed/?tag=${tag.slug}`"
          >
            <i class="fas fa-tags" /> {{ tag.name }}
          </router-link>
        </div>
      </div>
      <div class="blog-body" v-html="blogpage.body" />
    </div>
  </div>
</template>

<script>
  import PageTitle from "$components/PageTitle";
  import { blogpage_query } from "$store/queries";

  export default {
    components: { PageTitle },
    data() {
      return {
        blogpage: null,
      };
    },
    apollo: {
      blogpage: blogpage_query,
    },
  };
</script>

<style lang="scss"></style>
