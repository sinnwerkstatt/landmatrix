<template>
  <div>
    <PageTitle><span v-html="$t(pageTitle)"></span></PageTitle>
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

<script>
  import LoadingPulse from "$components/Data/LoadingPulse";
  import PageTitle from "$components/PageTitle";
  import { blogcategories_query, blogpages_query } from "$store/queries";

  export default {
    name: "BlogIndexPage",
    components: { LoadingPulse, PageTitle },
    data() {
      return {
        blogpages: null,
        blogcategories: [],
      };
    },
    apollo: { blogpages: blogpages_query, blogcategories: blogcategories_query },
    computed: {
      category() {
        return this.$route.query.category || null;
      },
      tag() {
        return this.$route.query.tag || null;
      },
      blogcategories_with_all() {
        return [{ slug: null, name: "All categories" }, ...this.blogcategories];
      },
      filtered_articles() {
        if (this.category) {
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
      pageTitle() {
        let title = this.$t(this.$store.state.page.wagtailPage.title);
        if (this.tag) {
          title += ` &nbsp;&nbsp;<small><i class="fas fa-tags"></i> ${this.tag}</small>`;
        }
        return title;
      },
    },
  };
</script>

<style lang="scss"></style>
