<script lang="ts">
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import { dealFields, investorFields } from "$lib/fieldLookups"
  import type { DealQIKey, InvestorQIKey } from "$lib/types/data"

  import IDField from "$components/Fields/Display2/IDField.svelte"
  import DisplayField from "$components/Fields/DisplayField.svelte"
  import Table from "$components/Table/Table.svelte"

  import { filters } from "../FilterBar.svelte"

  export let model: "deal" | "investor"
  export let key: DealQIKey | InvestorQIKey
  export let inverse: boolean

  $: dataPromise = $page.data.apiClient
    .GET(`/api/quality-indicators/${model}/`, {
      params: {
        query: {
          qi: key,
          inverse,
          region_id: $filters.region?.id,
          country_id: $filters.country?.id,
        },
      },
    })
    .then(res => ("error" in res ? Promise.reject(res.error) : res.data!))

  $: dealColumns = [
    { key: "id", colSpan: 1 },
    { key: "country_id", colSpan: 2 },
    { key: "deal_size", colSpan: 2 },
    { key: "current_intention_of_investment", colSpan: 4 },
    { key: "current_negotiation_status", colSpan: 4 },
    { key: "current_implementation_status", colSpan: 4 },
    { key: "created_at", colSpan: 2 },
    { key: "modified_at", colSpan: 2 },
    { key: "fully_updated_at", colSpan: 2 },
  ].map(c => ({ ...c, label: $dealFields[c.key].label }))

  $: investorColumns = [
    { key: "id", colSpan: 1 },
    { key: "country_id", colSpan: 5 },
    { key: "name", colSpan: 5 },
    { key: "created_at", colSpan: 2 },
    { key: "modified_at", colSpan: 2 },
  ].map(c => ({
    ...c,
    label: $investorFields[c.key].label,
  }))

  $: columns = model === "deal" ? dealColumns : investorColumns
</script>

{#await dataPromise}
  <div class="m-5">{$_("Loading...")}</div>
{:then data}
  <Table
    {columns}
    items={data}
    colWidthInPx={70}
    rowHeightInPx={54}
    headerHeightInPx={54}
  >
    <svelte:fragment let:fieldName let:obj slot="field">
      {#if fieldName === "id"}
        <IDField
          value={obj.id}
          extras={{
            targetBlank: true,
            objectVersion: obj.version_id,
            model: model,
          }}
        />
      {:else}
        <DisplayField
          value={obj[fieldName]}
          fieldname={fieldName}
          {model}
          wrapperClass="flex leading-5 gap-4"
          valueClass="text-gray-700 dark:text-white w-full"
        />
      {/if}
    </svelte:fragment>
  </Table>
{:catch error}
  <div class="m-5">{$_("Error")} {error}</div>
{/await}
