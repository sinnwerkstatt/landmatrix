<template>
  <li class="nav-item dropdown">
    <a
      id="searchDropdown"
      role="button"
      class="nav-link dropdown-toggle"
      data-toggle="dropdown"
      aria-haspopup="true"
      aria-expanded="false"
      @click="focusSearch"
    >
      <i class="fa fa-search"></i>
    </a>
    <div class="dropdown-menu search-menu" style="padding: 0.5rem 1rem">
      <form class="input-group">
        <label for="search" class="nowrap">
          {{ $t("Search deals and investors") }}
          <input
            id="search"
            v-model="search"
            type="text"
            class="form-control"
            :placeholder="$t('ID or Name')"
            @keydown="searchKeyboardEvent"
          />
        </label>
      </form>
      <ul v-if="searchResult.length > 0" id="ulle">
        <li
          v-for="(d, i) in searchResult"
          :id="`${d.id}${d.investor}`"
          :key="`${d.id}${d.investor}`"
          :class="{ investor: d.investor, selected: selectedSearchIndex === i }"
        >
          <router-link :class="{ not_public: d.is_public === false }" :to="d.url">
            {{ d.name }}
          </router-link>
        </li>
      </ul>
    </div>
  </li>
</template>
<script>
  import gql from "graphql-tag";

  export default {
    name: "NavbarSearch",
    data() {
      return {
        search: "",
        showSearch: false,
        selectedSearchIndex: 0,
        deals: [],
        investors: [],
      };
    },
    apollo: {
      deals: {
        query: gql`
          query SDeals($subset: Subset) {
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
      investors: {
        query: gql`
          query SInvestors($subset: Subset) {
            investors(limit: 0, subset: $subset) {
              id
              name
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
          return [
            ...this.deals
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
              }),
            ...this.investors
              .filter((i) => i.id.toString().includes(this.search))
              .map((i) => {
                return {
                  id: i.id,
                  name: `${i.name} #${i.id}`,
                  url: `/investor/${i.id}/`,
                  investor: true,
                };
              }),
          ];
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
      focusSearch() {
        setTimeout(() => document.getElementById("search").focus(), 100);
      },
      searchKeyboardEvent(e) {
        if (["ArrowDown", "ArrowUp"].includes(e.code)) {
          e.preventDefault();

          if (e.code === "ArrowDown") {
            this.selectedSearchIndex =
              (this.selectedSearchIndex + 1) % this.searchResult.length;
          } else {
            if (this.selectedSearchIndex === 0)
              this.selectedSearchIndex = this.searchResult.length - 1;
            else
              this.selectedSearchIndex =
                (this.selectedSearchIndex - 1) % this.searchResult.length;
          }

          let liel = this.searchResult[this.selectedSearchIndex];
          let offset = document.getElementById(`${liel.id}${liel.investor}`).offsetTop;
          document.getElementById("ulle").scrollTop = offset - 100;
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
      position: relative;
      max-height: 55vh;
      overflow-y: auto;
      margin: 1em 0 0;
      border-top: 1px solid var(--color-lm-orange);
      list-style: none;
      padding: 0.5em 0 0;
      li {
        &.selected {
          background: var(--color-lm-orange);
          a {
            color: white !important;
          }
        }
        &.investor {
          a {
            color: var(--color-lm-investor);
          }
        }
        &.investor.selected {
          background: var(--color-lm-investor);
          a {
            color: white !important;
          }
        }
      }
    }
  }
  .not_public {
    opacity: 0.4;
  }
</style>
