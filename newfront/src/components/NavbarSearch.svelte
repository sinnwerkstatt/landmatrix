<script lang="ts">
  import { gql } from "@apollo/client/core";
  import { _ } from "svelte-i18n";
  import { user } from "../lib/stores";

  let search = "";
  let showSearch = false;
  let selectedSearchIndex = 0;
  let deals = [];
  let investors = [];

  function getDeals() {
    let x = {
      query: gql`
        query SDeals($subset: Subset) {
          deals(limit: 0, subset: $subset) {
            id
            country {
              id
              name
            }
            is_public
          }
        }
      `,
      variables: {
        subset: $user?.is_authenticated ? "UNFILTERED" : "PUBLIC",
      },
    };
  }
  function getInvestors() {
    let x = {
      query: gql`
        query SInvestors($subset: Subset) {
          investors(limit: 0, subset: $subset) {
            id
            name
          }
        }
      `,
      variables: {
        subset: $user?.is_authenticated ? "UNFILTERED" : "PUBLIC",
      },
    };
  }

  let searchResult = [];
  // computed: {
  //   searchResult() {
  //     if (this.search.length >= 2) {
  //       return [
  //         ...this.deals
  //           .filter((d) => d.id.toString().includes(this.search))
  //           .map((d) => {
  //             let name = `#${d.id}`;
  //             if (d.country) name += ` in ${d.country?.name}`;
  //             return {
  //               id: d.id,
  //               name,
  //               is_public: d.is_public,
  //               url: `/deal/${d.id}/`,
  //             };
  //           }),
  //         ...this.investors
  //           .filter(
  //             (i) =>
  //               i.id.toString().includes(this.search) ||
  //               i.name.toLowerCase().includes(this.search.toLowerCase())
  //           )
  //           .map((i) => {
  //             return {
  //               id: i.id,
  //               name: `${i.name} #${i.id}`,
  //               url: `/investor/${i.id}/`,
  //               investor: true,
  //             };
  //           }),
  //       ];
  //     }
  //     return [];
  //   },
  // },
  // watch: {
  //   search(newS, oldS) {
  //     if (newS.length !== oldS.length) this.selectedSearchIndex = 0;
  //   },
  // },
  // methods: {
  function focusSearch() {
    setTimeout(() => document.getElementById("search").focus(), 100);
  }
  function searchKeyboardEvent(e) {
    if (["ArrowDown", "ArrowUp"].includes(e.code)) {
      e.preventDefault();

      if (e.code === "ArrowDown") {
        selectedSearchIndex = (selectedSearchIndex + 1) % searchResult.length;
      } else {
        if (selectedSearchIndex === 0) selectedSearchIndex = searchResult.length - 1;
        else selectedSearchIndex = (selectedSearchIndex - 1) % searchResult.length;
      }

      let liel = searchResult[selectedSearchIndex];
      let offset = document.getElementById(`${liel.id}${liel.investor}`).offsetTop;
      document.getElementById("ulle").scrollTop = offset - 100;
    }

    if (e.code === "Enter") {
      // $router.push(searchResult[selectedSearchIndex].url);
      e.preventDefault();
      document.getElementById("searchDropdown").click();
    }
  }
  // },
</script>

<li class="nav-item dropdown">
  <a
    id="searchDropdown"
    role="button"
    class="nav-link dropdown-toggle"
    data-toggle="dropdown"
    aria-haspopup="true"
    aria-expanded="false"
    on:click={focusSearch}
  >
    <i class="fa fa-search" />
  </a>
  <div class="dropdown-menu search-menu" style="padding: 0.5rem 1rem">
    <form class="input-group">
      <label for="search" class="whitespace-nowrap">
        {$_("Search deals and investors")}
        <input
          id="search"
          bind:value={search}
          type="text"
          class="form-control"
          placeholder={$_("ID or Name")}
          on:keydown={searchKeyboardEvent}
        />
      </label>
    </form>
    {#if searchResult.length > 0}
      <ul id="ulle">
        {#each searchResult as d, i}
          <li
            id="{d.id}{d.investor}"
            class:investor={d.investor}
            class:selected={selectedSearchIndex === i}
          >
            <a class:not_public={d.is_public === false} href={d.url}>
              {d.name}
            </a>
          </li>
        {/each}
      </ul>
    {/if}
  </div>
</li>

<!--<style scoped lang="scss">-->
<!--  .search-menu {-->
<!--    //max-height: 60vh;-->

<!--    ul {-->
<!--      position: relative;-->
<!--      max-height: 55vh;-->
<!--      overflow-y: auto;-->
<!--      margin: 1em 0 0;-->
<!--      border-top: 1px solid var(&#45;&#45;color-lm-orange);-->
<!--      list-style: none;-->
<!--      padding: 0.5em 0 0;-->
<!--      li {-->
<!--        &.selected {-->
<!--          background: var(&#45;&#45;color-lm-orange);-->
<!--          a {-->
<!--            color: white !important;-->
<!--          }-->
<!--        }-->
<!--        &.investor {-->
<!--          a {-->
<!--            color: var(&#45;&#45;color-lm-investor);-->
<!--          }-->
<!--        }-->
<!--        &.investor.selected {-->
<!--          background: var(&#45;&#45;color-lm-investor);-->
<!--          a {-->
<!--            color: white !important;-->
<!--          }-->
<!--        }-->
<!--      }-->
<!--    }-->
<!--  }-->
<!--  .not_public {-->
<!--    opacity: 0.4;-->
<!--  }-->
<!--</style>-->
