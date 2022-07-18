<script lang="ts">
  import { gql } from "graphql-tag";
  import { _ } from "svelte-i18n";
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";
  import { client } from "$lib/apolloClient";
  import type { Deal } from "$lib/types/deal";
  import type { Investor } from "$lib/types/investor";
  import SearchIcon from "./icons/SearchIcon.svelte";
  import NavDropDown from "./LowLevel/NavDropDown.svelte";

  $: user = $page.stuff.user;

  let search = "";
  let showSearch = false;
  let selectedSearchIndex = 0;
  let deals: Deal[] = [];
  let investors: Investor[] = [];

  async function getDeals() {
    const { data } = await $client.query<{ deals: Deal[] }>({
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
        subset: user?.is_authenticated ? "UNFILTERED" : "PUBLIC",
      },
    });
    deals = data.deals;
  }

  async function getInvestors() {
    const { data } = await $client.query<{ investors: Investor[] }>({
      query: gql`
        query SInvestors($subset: Subset) {
          investors(limit: 0, subset: $subset) {
            id
            name
          }
        }
      `,
      variables: { subset: user?.is_authenticated ? "UNFILTERED" : "PUBLIC" },
    });
    investors = data.investors;
  }

  getDeals();
  getInvestors();

  $: searchResult =
    search.length >= 2
      ? [
          ...deals
            .filter((d) => d.id.toString().includes(search))
            .map((d) => {
              let name = `#${d.id}`;
              if (d.country) name += ` in ${d.country?.name}`;
              return { id: d.id, name, is_public: d.is_public, url: `/deal/${d.id}/` };
            }),
          ...investors
            .filter(
              (i) =>
                i.id.toString().includes(search) ||
                i.name.toLowerCase().includes(search.toLowerCase())
            )
            .map((i) => {
              return {
                id: i.id,
                name: `${i.name} #${i.id}`,
                url: `/investor/${i.id}/`,
                investor: true,
              };
            }),
        ]
      : [];
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
      goto(searchResult[selectedSearchIndex].url);
      e.preventDefault();
      document.getElementById("searchDropdown").click();
    }
  }
  // },
</script>

<NavDropDown>
  <div slot="title">
    <SearchIcon class="h-5 w-5 mr-2" />
  </div>
  <div class="border border-orange bg-white py-2 px-4">
    <form>
      <label for="search" class="whitespace-nowrap flex flex-col">
        {$_("Search deals and investors")}
        <input
          id="search"
          bind:value={search}
          type="text"
          class="inpt"
          placeholder={$_("ID or Name")}
          on:keydown={searchKeyboardEvent}
        />
      </label>
    </form>
    {#if searchResult.length > 0}
      <ul
        id="ulle"
        class="relative max-h-[55vh] overflow-y-auto mt-4 pt-2 border-t-orange"
      >
        {#each searchResult as d, i}
          <li>
            <a
              href={d.url}
              class={selectedSearchIndex === i
                ? d.investor
                  ? "bg-pelorous"
                  : "bg-orange"
                : d.investor
                ? "text-pelorous"
                : "text-orange"}
              class:opacity-40={d.is_public === false}
              class:text-white={selectedSearchIndex === i}
            >
              {d.name}
            </a>
          </li>
        {/each}
      </ul>
    {/if}
  </div>
</NavDropDown>
