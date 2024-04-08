<script lang="ts">
  import { page } from "$app/stores"

  import type { InvestorHull } from "$lib/types/newtypes"

  import CountryField from "$components/Fields/Display2/CountryField.svelte"

  let value = ""

  let actives: InvestorHull[] = []
  let drafts: InvestorHull[] = []
  async function getSearchResults(v: string) {
    if (v.length < 3) {
      actives = []
      drafts = []
      return
    }
    const req = await $page.data.apiClient.GET("/api/investor_search", {
      params: { query: { q: v } },
    })
    if (req.error) error(500, req.error)
    actives = req.data.filter(i => i.active_version_id)
    drafts = req.data.filter(i => i.draft_version_id)
  }
  $: getSearchResults(value)
</script>

<div class="mt-12 flex w-full items-center justify-center">
  <h1>Investor search</h1>
</div>

<div class="container mx-auto">
  <form class="flex justify-center">
    <input bind:value class="inpt w-1/2" placeholder="" />
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
      Drafts:

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
