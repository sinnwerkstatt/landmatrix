<script lang="ts">
  import { gql } from "@urql/svelte"
  import cn from "classnames"
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { goto } from "$app/navigation"
  import { page } from "$app/stores"

  import type { Deal } from "$lib/types/deal"
  import type { Investor } from "$lib/types/investor"

  import NavDropDown from "$components/Navbar/NavDropDown.svelte"

  import SearchIcon from "../icons/SearchIcon.svelte"

  $: user = $page.data.user

  interface SearchResult {
    id: number
    name: string
    url: string
    is_public?: boolean
    investor?: boolean
  }

  let searchString = ""
  let selectedSearchIndex = 0
  let searchResult: SearchResult[] = []
  let searchResultContainer: HTMLUListElement
  let deals: Deal[] = []
  let investors: Investor[] = []

  async function getDeals() {
    const { error, data } = await $page.data.urqlClient
      .query<{ deals: Deal[] }>(
        gql`
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
        {
          subset: user?.is_authenticated ? "UNFILTERED" : "PUBLIC",
        },
      )
      .toPromise()

    if (error || !data) {
      console.error(error)
      return
    }

    deals = data.deals
  }

  async function getInvestors() {
    const { error, data } = await $page.data.urqlClient
      .query<{ investors: Investor[] }>(
        gql`
          query SInvestors($subset: Subset) {
            investors(
              limit: 0
              subset: $subset
              filters: [{ field: "status", value: 4, exclusion: true }]
            ) {
              id
              name
            }
          }
        `,
        { subset: user?.is_authenticated ? "UNFILTERED" : "PUBLIC" },
      )
      .toPromise()

    if (error || !data) {
      console.error(error)
      return
    }

    investors = data.investors
  }

  $: {
    // on search change
    selectedSearchIndex = 0
    searchResult =
      searchString.length >= 2
        ? [
            ...deals
              .filter(d => d.id.toString().includes(searchString))
              .map<SearchResult>(d => {
                let name = `#${d.id}`
                if (d.country) name += ` in ${d.country?.name}`
                return {
                  id: d.id,
                  name,
                  is_public: d.is_public,
                  url: `/deal/${d.id}/`,
                }
              }),
            ...investors
              .filter(
                i =>
                  i.id.toString().includes(searchString) ||
                  i.name.toLowerCase().includes(searchString.toLowerCase()),
              )
              .map<SearchResult>(i => {
                return {
                  id: i.id,
                  name: `${i.name} #${i.id}`,
                  url: `/investor/${i.id}/`,
                  investor: true,
                }
              }),
          ]
        : []
  }

  function searchKeyboardEvent(e) {
    if (["ArrowDown", "ArrowUp", "Enter"].includes(e.code)) {
      e.preventDefault()

      if (!searchResult.length) {
        return
      }

      switch (e.code) {
        case "ArrowDown":
          selectedSearchIndex = (selectedSearchIndex + 1) % searchResult.length
          searchResultContainer.children[selectedSearchIndex].scrollIntoView(false)
          return
        case "ArrowUp":
          selectedSearchIndex =
            selectedSearchIndex === 0
              ? searchResult.length - 1
              : selectedSearchIndex - 1
          searchResultContainer.children[selectedSearchIndex].scrollIntoView(false)
          return
        case "Enter":
          goto(searchResult[selectedSearchIndex].url)
          return
        default:
          return
      }
    }
  }

  onMount(() => {
    getDeals()
    getInvestors()
  })
</script>

<NavDropDown>
  <svelte:fragment slot="title">
    <div
      class="flex items-center justify-end bg-white px-2 dark:bg-lm-black lg:w-[250px]"
    >
      <input
        id="search"
        bind:value={searchString}
        class="inpt mr-3 hidden rounded xl:block"
        placeholder={$_("Search for...")}
        autocomplete="off"
        on:keydown={searchKeyboardEvent}
      />
      <SearchIcon class="h-6" />
    </div>
  </svelte:fragment>
  <div
    class="relative w-[300px] rounded bg-white p-2 shadow-lg dark:bg-lm-black xl:hidden"
  >
    <input
      id="search"
      bind:value={searchString}
      class="inpt"
      placeholder={$_("Search")}
      autocomplete="off"
      on:keydown={searchKeyboardEvent}
    />
  </div>
  {#if searchResult.length}
    <ul
      bind:this={searchResultContainer}
      id="search-result"
      class={cn(
        "w-full overflow-y-auto border-t-orange",
        "bg-white dark:bg-gray-800",
        "xl:absolute xl:z-50 xl:max-h-[55vh] xl:w-[300px]",
        "xl:shadow-xl",
      )}
    >
      {#each searchResult.filter((item, index) => index < 10) as item, index}
        <li>
          <a
            href={item.url}
            class={cn(
              "block border-2 px-1.5 py-1 transition duration-100 hover:text-white",
              selectedSearchIndex === index ? "border-gray-200" : "border-transparent",
              item.investor
                ? "text-pelorous hover:bg-pelorous"
                : "text-orange hover:bg-orange",
            )}
            class:opacity-40={!item.investor && !item.is_public}
          >
            {item.name}
          </a>
        </li>
      {/each}
    </ul>
  {/if}
</NavDropDown>

<style>
  :global(#search + button) {
    margin-left: -30px;
  }
</style>
