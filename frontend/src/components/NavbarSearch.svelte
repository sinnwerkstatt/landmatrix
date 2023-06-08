<script lang="ts">
  import { gql, Client } from "@urql/svelte"
  import classNames from "classnames"
  import { _ } from "svelte-i18n"
  import { onMount } from "svelte"

  import { goto } from "$app/navigation"
  import { page } from "$app/stores"

  import type { Deal } from "$lib/types/deal"
  import type { Investor } from "$lib/types/investor"

  import SearchIcon from "./icons/SearchIcon.svelte"
  import NavDropDown from "./LowLevel/NavDropDown.svelte"

  $: user = $page.data.user

  interface SearchResult {
    id: number
    name: string
    url: string
    is_public?: boolean
    investor?: boolean
  }

  let search = ""
  let selectedSearchIndex = 0
  let searchResult: SearchResult[] = []
  let searchResultContainer: HTMLUListElement
  let deals: Deal[] = []
  let investors: Investor[] = []

  async function getDeals() {
    const { error, data } = await ($page.data.urqlClient as Client)
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
    const { error, data } = await ($page.data.urqlClient as Client)
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
      search.length >= 2
        ? [
            ...deals
              .filter(d => d.id.toString().includes(search))
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
                  i.id.toString().includes(search) ||
                  i.name.toLowerCase().includes(search.toLowerCase()),
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
          searchResultContainer.children[selectedSearchIndex].scrollIntoView()
          return
        case "ArrowUp":
          selectedSearchIndex =
            selectedSearchIndex === 0
              ? searchResult.length - 1
              : selectedSearchIndex - 1
          searchResultContainer.children[selectedSearchIndex].scrollIntoView()
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

<NavDropDown placement="right-0">
  <div slot="title">
    <SearchIcon class="mr-2 h-5 w-5" />
  </div>
  <div class="border border-orange bg-white py-2 px-4 dark:bg-gray-800">
    <form>
      <label for="search" class="flex flex-col whitespace-nowrap">
        {$_("Search deals and investors")}
        <input
          id="search"
          bind:value={search}
          type="text"
          class="inpt"
          placeholder={$_("ID or Name")}
          autocomplete="off"
          on:keydown={searchKeyboardEvent}
        />
      </label>
    </form>
    <ul
      bind:this={searchResultContainer}
      id="search-result"
      class="relative mt-4 max-h-[55vh] overflow-y-auto border-t-orange pt-2"
    >
      {#each searchResult as item, index}
        <li>
          <a
            href={item.url}
            class={classNames(
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
  </div>
</NavDropDown>
