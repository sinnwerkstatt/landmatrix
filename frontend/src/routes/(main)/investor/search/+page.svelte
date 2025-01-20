<script lang="ts">
  import { error } from "@sveltejs/kit"
  import { _ } from "svelte-i18n"

  import { page } from "$app/state"

  import type { SearchedInvestor } from "$lib/types/data"

  import CountryField from "$components/Fields/Display2/CountryField.svelte"

  let value = $state("")

  let actives: SearchedInvestor[] = $state([])
  let drafts: SearchedInvestor[] = $state([])

  async function getSearchResults() {
    if (value.length < 3) {
      actives = []
      drafts = []
      return
    }
    const req = await page.data.apiClient.GET("/api/investor_search/", {
      params: { query: { q: value } },
    })
    if ("error" in req) error(500, req.error)
    actives = req.data.filter(i => i.active_version_id)
    drafts = req.data.filter(i => i.draft_version_id)
  }
</script>

<div class="mt-12 flex w-full items-center justify-center">
  <h1>{$_("Investor search")}</h1>
</div>

<div class="container mx-auto">
  <form class="flex justify-center">
    <input bind:value oninput={getSearchResults} class="inpt w-1/2" placeholder="" />
  </form>

  <div class="mt-10">
    <ul class="mb-12">
      {#each actives as investor}
        <li class="py-0.5 odd:bg-gray-100">
          <a class="investor flex" href="/investor/{investor.id}/" target="_blank">
            <span class="w-[5rem]">[{investor.id}]</span>
            <span class="min-w-[10rem] px-4">
              <CountryField value={investor.selected_version.country_id} />
            </span>
            {investor.selected_version.name}
          </a>
        </li>
      {/each}
    </ul>
    {#if drafts.length}
      {$_("Drafts")}:

      <ul>
        {#each drafts as investor}
          <li class="py-0.5 odd:bg-gray-100">
            <a class="investor flex" href="/investor/{investor.id}/" target="_blank">
              <span class="w-[5rem]">[{investor.id}]</span>
              <span class="min-w-[10rem] px-4">
                <CountryField value={investor.selected_version.country_id} />
              </span>
              {investor.selected_version.name}
            </a>
          </li>
        {/each}
      </ul>
    {/if}
  </div>
</div>
