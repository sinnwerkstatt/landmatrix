<script lang="ts">
  import { _ } from "svelte-i18n"

  import { browser } from "$app/environment"
  import { page } from "$app/stores"

  import type { InvestorHull } from "$lib/types/data"

  import CountryField from "$components/Fields/Display2/CountryField.svelte"

  export let value: InvestorHull | number | null

  export const extras = {}

  const fetchInvestor = async (value: InvestorHull | number): Promise<InvestorHull> => {
    if (typeof value === "number") {
      const ret = await $page.data.apiClient.GET("/api/investors/{id}/", {
        params: { path: { id: value } },
      })
      if (ret.error) {
        // @ts-expect-error openapi-fetch types broken
        throw new Error(ret.error)
      }

      return ret.data as unknown as InvestorHull
    }

    return value
  }
</script>

<!-- Need to add browser here. During SSR the fetch somehow returns 404 -->
{#if browser && value}
  {#await fetchInvestor(value)}
    <span>{$_("Loading")}</span>
  {:then investor}
    {#if investor.deleted}
      <span class="font-bold text-red">
        {$_("Deleted")}:
      </span>
    {:else if investor.active_version_id === null}
      <span class="font-bold text-purple">
        {$_("Draft")}:
      </span>
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
    <!-- eslint-disable-next-line @typescript-eslint/no-unused-vars -->
  {:catch error}
    <span class="text-red">{$_("Investor not found")} #{value}</span>
  {/await}
{/if}
