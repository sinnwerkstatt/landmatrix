<template>
  <li class="nav-item dropdown">
    <a
      id="searchDropdown"
      role="button"
      class="nav-link dropdown-toggle"
      data-toggle="dropdown"
      aria-haspopup="true"
      aria-expanded="false"
    >
      <i class="fa fa-search"></i>
    </a>
    <div class="dropdown-menu search-menu" style="padding: 0.5rem 1rem">
      <form class="input-group">
        <label for="search" style="white-space: nowrap">
          Search for deals and investors
        </label>
        <input
          id="search"
          ref="searchInput"
          v-model="search"
          type="text"
          class="form-control"
          placeholder="ID or Name"
          @keydown="searchKeyboardEvent"
        />
      </form>
      <ul v-if="searchResult.length > 0">
        <li
          v-for="(d, i) in searchResult"
          :key="d.id"
          :class="{ selected: selectedSearchIndex === i }"
        >
          <router-link :class="{ not_public: !d.is_public }" :to="d.url">
            {{ d.name }}
          </router-link>
        </li>
      </ul>
    </div>
  </li>
</template>
<script>
  import { blogcategories_query } from "$store/queries";
  import gql from "graphql-tag";

  export default {
    name: "NavbarSearch",
    data() {
      return {
        search: "",
        showSearch: false,
        selectedSearchIndex: 0,
        deals: [],
      };
    },
    apollo: {
      blogcategories: blogcategories_query,
      deals: {
        query: gql`
          query Deals($subset: Subset) {
            deals(limit: 0, subset: $subset) {
              id
              country {
                name
              }
              is_public
            }
          }
        `,
        variables() {
          return {
            subset: this.$store.getters.userAuthenticated ? "UNFILTERED" : "PUBLIC",
          };
        },
      },
    },
    computed: {
      searchResult() {
        if (this.search.length >= 2) {
          return this.deals
            .filter((d) => d.id.toString().includes(this.search))
            .map((d) => {
              let name = `#${d.id}`;
              if (d.country) name += ` in ${d.country?.name}`;
              return {
                id: d.id,
                name,
                is_public: d.is_public,
                url: `/deal/${d.id}/`,
              };
            });
        }
        return [];
      },
    },
    watch: {
      search(newS, oldS) {
        if (newS.length !== oldS.length) this.selectedSearchIndex = 0;
      },
    },
    methods: {
      searchKeyboardEvent(e) {
        if (e.code === "ArrowDown") {
          this.selectedSearchIndex =
            (this.selectedSearchIndex + 1) % this.searchResult.length;
          e.preventDefault();
        }
        if (e.code === "ArrowUp") {
          if (this.selectedSearchIndex === 0)
            this.selectedSearchIndex = this.searchResult.length - 1;
          else
            this.selectedSearchIndex =
              (this.selectedSearchIndex - 1) % this.searchResult.length;
          e.preventDefault();
        }
        if (e.code === "Enter") {
          this.$router.push(this.searchResult[this.selectedSearchIndex].url);
          e.preventDefault();
          document.getElementById("searchDropdown").click();
        }
      },
    },
  };
</script>

<style scoped lang="scss">
  .search-menu {
    //max-height: 60vh;

    ul {
      max-height: 55vh;
      overflow-y: auto;
      margin: 1em 0 0;
      border-top: 1px solid var(--color-lm-orange);
      list-style: none;
      padding: 0.5em 0 0;
      li.selected {
        background: var(--color-lm-orange);
        a {
          color: white !important;
        }
      }
    }
  }
  .not_public {
    opacity: 0.4;
  }
</style>
