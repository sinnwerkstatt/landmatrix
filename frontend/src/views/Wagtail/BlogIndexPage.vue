<template>
  <div v-if="blogpages" class="container">
    <div class="row">
      <div class="col">
        <label v-for="cat in blogcategories_with_all">
          <input
            type="radio"
            v-model="category"
            :value="cat.slug"
            name="categoryRadio"
          />
          {{ $t(cat.name) }}
        </label>
      </div>
    </div>
    <div class="row">
      <div v-for="article in filtered_articles" class="col-4 mb-3">
        <div class="card">
          <img
            v-if="article.header_image"
            :src="article.header_image"
            class="card-img-top"
            alt="Card image cap"
          />
          <div class="card-body">
            <h5 class="card-title">
              <router-link :to="`/stay-informed/${article.slug}`">{{
                article.title
              }}</router-link>
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
</template>

<script>
  import axios from "axios";
  import gql from "graphql-tag";

  export default {
    data() {
      return {
        blogpages: null,
        category: null,
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
        return this.blogpages;
      },
    },
  };
</script>

<style lang="scss"></style>
