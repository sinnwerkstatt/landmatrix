<template>
  <div>
    <PageTitle>
      <span>{{ $t($store.state.page.wagtailPage.title) }}</span>
      <small v-if="tag"><i class="fas fa-tags"></i> {{ tag }}</small>
    </PageTitle>
    <div class="container">
      <LoadingPulse v-if="$apollo.queries.blogpages.loading" />
      <!--    <div class="row " v-if="tag">-->
      <!--      <div class="col text-center">-->
      <!--        <i class="fas fa-tags"></i> {{tag}}-->
      <!--      </div>-->
      <!--    </div>-->
      <div v-if="blogcategories_with_all" class="row mb-4">
        <div class="col text-center">
          <ul class="nav nav-pills d-flex justify-content-center">
            <li v-for="cat in blogcategories_with_all" :key="cat.slug" class="nav-item">
              <router-link
                :class="{ active: category === cat.slug }"
                :to="cat.slug ? `?category=${cat.slug}` : './'"
                class="nav-link"
              >
                {{ $t(cat.name) }}
              </router-link>
            </li>
          </ul>
        </div>
      </div>
      <div v-if="blogpages" class="row">
        <div
          v-for="article in filtered_articles"
          :key="article.slug"
          class="col-md-6 col-lg-4 mb-3"
        >
          <div class="card">
            <img
              v-if="article.header_image"
              :src="article.header_image"
              alt="Card image cap"
              class="card-img-top"
            />
            <div class="card-body">
              <h5 class="card-title">
                <router-link :to="article.url">
                  {{ article.title }}
                </router-link>
              </h5>
              <!-- eslint-disable-next-line vue/no-v-html -->
              <p class="card-text" v-html="article.excerpt" />
              <p class="card-text">
                <small class="text-muted">{{ article.date }}</small>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
  import LoadingPulse from "$components/Data/LoadingPulse.vue";
  import PageTitle from "$components/PageTitle.vue";
  import { blogcategories_query, blogpages_query } from "$store/queries";
  import Vue from "vue";
  import type { BlogCategory, BlogPage } from "$types/wagtail";

  export default Vue.extend({
    name: "BlogIndexPage",
    components: { LoadingPulse, PageTitle },
    data() {
      return {
        blogpages: [] as BlogPage[],
        blogcategories: [] as BlogCategory[],
      };
    },
    apollo: { blogpages: blogpages_query, blogcategories: blogcategories_query },
    computed: {
      category(): string | null {
        return this.$route.query?.category?.toString() || null;
      },
      tag(): string | null {
        return this.$route.query?.tag?.toString() || null;
      },
      blogcategories_with_all(): BlogCategory[] {
        return [{ id: -1, slug: null, name: "All categories" }, ...this.blogcategories];
      },
      filtered_articles(): BlogPage[] {
        if (this.category && this.blogpages.length > 0) {
          return this.blogpages.filter((art) =>
            art.categories.map((c) => c.slug).includes(this.category)
          );
        }
        if (this.tag) {
          return this.blogpages.filter((art) =>
            art.tags.map((c) => c.slug).includes(this.tag)
          );
        }
        return this.blogpages;
      },
    },
  });
</script>
