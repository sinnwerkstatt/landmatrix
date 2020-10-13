<template>
  <div>
    <PageTitle :title="pageTitle()"></PageTitle>
    <div class="container">
      <LoadingPulse v-if="$apollo.queries.blogpages.loading" />
      <!--    <div class="row " v-if="tag">-->
      <!--      <div class="col text-center">-->
      <!--        <i class="fas fa-tags"></i> {{tag}}-->
      <!--      </div>-->
      <!--    </div>-->
      <div class="row mb-4" v-if="blogcategories_with_all">
        <div class="col text-center">
          <ul class="nav nav-pills d-flex justify-content-center">
            <li class="nav-item" v-for="cat in blogcategories_with_all">
              <router-link
                class="nav-link"
                :class="{ active: category === cat.slug }"
                :to="cat.slug ? `?category=${cat.slug}` : './'"
                >{{ $t(cat.name) }}</router-link
              >
            </li>
          </ul>
        </div>
      </div>
      <div class="row" v-if="blogpages">
        <div v-for="article in filtered_articles" class="col-md-6 col-lg-4 mb-3">
          <div class="card">
            <img
              v-if="article.header_image"
              :src="article.header_image"
              class="card-img-top"
              alt="Card image cap"
            />
            <div class="card-body">
              <h5 class="card-title">
                <router-link :to="`${article.slug}/`">{{ article.title }}</router-link>
              </h5>
              <p class="card-text" v-html="article.excerpt"></p>
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
  import gql from "graphql-tag";
  import LoadingPulse from "../../components/Data/LoadingPulse";
  import PageTitle from "../../components/PageTitle";

  export default {
    components: { LoadingPulse, PageTitle },
    data() {
      return {
        blogpages: null,
        category: null,
        tag: null,
        blogcategories: [],
      };
    },
    apollo: {
      blogpages: gql`
        query {
          blogpages {
            id
            title
            slug
            date
            header_image
            excerpt
            categories {
              slug
            }
            tags {
              slug
            }
          }
        }
      `,
      blogcategories: gql`
        query {
          blogcategories {
            id
            name
            slug
          }
        }
      `,
    },
    computed: {
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
    },
    methods: {
      pageTitle() {
        this.category = this.$route.query.category || null;
        this.tag = this.$route.query.tag || null;
        let title = "Stay Informed";
        if (this.tag) {
          title += ` - &nbsp;<span class="small"><i class="fas fa-tags"></i>${this.tag}</span>`
        }
        return title;
      },
      updatePageTitle() {
        this.$store.commit(
          "setTitle",
          this.pageTitle()
        );
      }
    },
    mounted() {
      this.updatePageTitle();
    },
    watch: {
      $route(to, from) {
        this.updatePageTitle();
      },
    },
  };
</script>

<style lang="scss"></style>
