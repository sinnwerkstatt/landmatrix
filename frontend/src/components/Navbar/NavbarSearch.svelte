<script lang="ts">
  import { gql } from "@urql/svelte"
  import { _ } from "svelte-i18n"
  import { onMount } from "svelte"
  import cn from "classnames"

  import { goto } from "$app/navigation"
  import { page } from "$app/stores"

  import type { Deal } from "$lib/types/deal"
  import type { Investor } from "$lib/types/investor"

  import XIcon from "$components/icons/XIcon.svelte"

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
    const { data } = await $page.data.urqlClient
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
    deals = data?.deals ?? []
  }

  async function getInvestors() {
    const { data } = await $page.data.urqlClient
      .query<{ investors: Investor[] }>(
        gql`
          query SInvestors($subset: Subset) {
            investors(limit: 0, subset: $subset) {
              id
              name
            }
          }
        `,
        { subset: user?.is_authenticated ? "UNFILTERED" : "PUBLIC" },
      )
      .toPromise()
    investors = data?.investors ?? []
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

<div class="relative my-auto">
  <div class="flex w-[200px] px-2">
    <input
      id="search"
      bind:value={searchString}
      class="inpt my-auto"
      placeholder={$_("Search")}
      autocomplete="off"
      on:keydown={searchKeyboardEvent}
    />
    <button
      on:click={() => {
        searchString = ""
      }}
    >
      {#if searchString !== ""}
        <XIcon class="my-auto inline h-5 w-5" />
      {:else}
        <SearchIcon class="my-auto inline h-5 w-5" />
      {/if}
    </button>
  </div>

  {#if searchResult.length}
    <ul
      bind:this={searchResultContainer}
      id="search-result"
      class={cn(
        "right-0 w-full overflow-y-auto border-t-orange",
        "bg-white dark:bg-gray-800",
        "xl:absolute xl:z-50 xl:max-h-[55vh] xl:w-[300px]",
        "xl:border-2 xl:border-orange xl:shadow-xl",
      )}
    >
      {#each searchResult.filter((item, index) => index < 10) as item, index}
        <li>
          <a
            href={item.url}
            class={cn(
              "block border-2 py-1 px-1.5 transition duration-100 hover:text-white",
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
</div>

<style>
  :global(#search + button) {
    margin-left: -30px;
  }
</style>
