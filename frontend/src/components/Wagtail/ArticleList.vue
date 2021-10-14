<template>
  <div v-if="articles.length" class="articles clamp-20-75p-56">
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
      {{ $t("Show all") }} {{ articles.length }} {{ articlesLabel.toLowerCase() }}
    </button>
  </div>
</template>

<script lang="ts">
  import Vue, { PropType } from "vue";
  import type { BlogPage } from "$types/wagtail";

  export default Vue.extend({
    name: "ArticleList",
    props: {
      articles: { type: Array as PropType<BlogPage[]>, required: true },
      articlesLabel: { type: String, required: true },
    },
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
  });
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
    img {
      max-width: 100%;
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
