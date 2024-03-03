<script lang="ts">
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import type { InvestorHull } from "$lib/types/newtypes"

  import CountryField from "$components/Fields/Display2/CountryField.svelte"

  export let value: InvestorHull | number | null

  let investor: InvestorHull | null

  async function fetchInvestor() {
    if (value === null) return
    if (typeof value === "number") {
      const ret = await fetch(`/api/investors/${value}/`)
      investor = await ret.json()
    } else {
      investor = value
    }
  }

  onMount(() => {
    fetchInvestor()
  })
</script>

{#if investor}
  {#if !investor.active_version_id}
    {$_("Draft")}:
  {/if}
  <a href="/investor/{investor.id}/" class="investor">
    {#if investor.selected_version.name_unknown}
      <span class="italic">[{$_("unknown investor")}]</span>
    {:else}
      {investor.selected_version.name}
    {/if}
    #{investor.id}
    {#if investor.selected_version.country_id}
      - <CountryField value={investor.selected_version.country_id} />
    {/if}
  </a>
{:else if value}
  <a href="/investor/{value}/" class="investor">
    {$_("Investor")} #{value}
  </a>
{/if}
