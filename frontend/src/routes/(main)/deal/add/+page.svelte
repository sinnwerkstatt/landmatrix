<script lang="ts">
  import { goto } from "$app/navigation"
  import { page } from "$app/stores"

  import type { components } from "$lib/openAPI"
  import { getCsrfToken } from "$lib/utils"

  import CountrySelect from "$components/LowLevel/CountrySelect.svelte"

  let country: components["schemas"]["Country"]

  async function createDraft() {
    const ret = await fetch("/api/deals/", {
      method: "POST",
      credentials: "include",
      body: JSON.stringify({ country_id: country.id }),
      headers: {
        "X-CSRFToken": await getCsrfToken(),
        "Content-Type": "application/json",
      },
    })
    if (ret.ok) {
      const retJson = await ret.json()
      await goto(`/deal/edit/${retJson.dealID}/${retJson.versionID}/`)
    }
  }
</script>

<form class="container mx-auto py-8" on:submit|preventDefault={createDraft}>
  <h1 class="heading1 my-8">Adding a new deal</h1>

  <div class="mt-16 flex flex-wrap gap-4">
    <p class="heading5">First, choose the country where the deal is located.</p>
    <CountrySelect
      bind:value={country}
      countries={$page.data.countries.filter(c => !c.high_income)}
    />
  </div>
  <div class="my-6">
    <button class="btn btn-primary w-full" disabled={!country} type="submit">
      Add a new deal
    </button>
  </div>
</form>
