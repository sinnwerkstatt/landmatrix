<template>
  <div v-if="articles.length" class="articles container">
    <div class="row justify-content-center">
      <div class="col-sm-12 col-md-10 col-lg-8 col-xl-6">
        <h3>{{ $t(articlesLabel) }}</h3>
        <slot />
        <div v-for="article in limitedArticles" :key="article.slug">
          <div class="article row">
            <div class="col-3">
              <img
                v-if="article.header_image"
                :src="article.header_image"
                :alt="`Header image for ${article.title}`"
              />
            </div>
            <div class="col-9">
              <h5 class="title">
                <router-link :to="article.url">{{ article.title }}</router-link>
              </h5>
              <div class="excerpt" v-html="article.excerpt"></div>
            </div>
          </div>
        </div>
        <button v-if="limit && limit < articles.length" @click.prevent="limit = 0">
          Show all {{ articles.length }} {{ articlesLabel.toLowerCase() }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "ArticleListe",
    props: ["articles", "articlesLabel"],
    data() {
      return {
        limit: 3,
      };
    },
    computed: {
      limitedArticles() {
        if (this.limit) {
          return this.articles.slice(0, this.limit);
        } else {
          return this.articles;
        }
      },
    },
  };
</script>

<style lang="scss" scoped>
  .articles {
    margin-top: 2em;
    margin-bottom: 2em;
    h4 {
      font-size: 18px;
      margin-bottom: 1.2em;
    }
    h5 {
      font-size: 18px;
      a {
        color: var(--color-lm-orange);
      }
    }
    .article {
      img {
        height: auto;
      }
      margin-bottom: 1em;
    }
    button {
      border: 1px solid black;
      padding: 0.2em 1.2em;
      font-size: 14px;
      text-transform: uppercase;
      color: black;
    }
  }
</style>
