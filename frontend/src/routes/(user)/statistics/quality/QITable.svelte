<script lang="ts">
  import { _ } from "svelte-i18n"

  import { page } from "$app/state"

  import { dealFields, investorFields } from "$lib/fieldLookups"
  import { filters } from "$lib/filters"
  import type { DealQIKey, InvestorQIKey, Model } from "$lib/types/data"

  import IDField from "$components/Fields/Display2/IDField.svelte"
  import DisplayField from "$components/Fields/DisplayField.svelte"
  import Table from "$components/Table/Table.svelte"

  interface Props {
    model: Model
    key: DealQIKey | InvestorQIKey
    inverse: boolean
  }

  let { model, key, inverse }: Props = $props()

  let dataPromise = $derived(
    page.data.apiClient
      .GET(`/api/quality-indicators/${model}/`, {
        params: {
          query: {
            qi: key,
            inverse,
            region_id: $filters.region_id,
            country_id: $filters.country_id,
          },
        },
      })
      .then(res => ("error" in res ? Promise.reject(res.error) : res.data!)),
  )

  let dealColumns = $derived(
    [
      { key: "id", colSpan: 1 },
      { key: "country_id", colSpan: 2 },
      { key: "deal_size", colSpan: 2 },
      { key: "current_intention_of_investment", colSpan: 4 },
      { key: "current_negotiation_status", colSpan: 4 },
      { key: "current_implementation_status", colSpan: 4 },
      { key: "created_at", colSpan: 2 },
      { key: "modified_at", colSpan: 2 },
      { key: "fully_updated_at", colSpan: 2 },
    ].map(c => ({ ...c, label: $dealFields[c.key].label })),
  )

  let investorColumns = $derived(
    [
      { key: "id", colSpan: 1 },
      { key: "country_id", colSpan: 5 },
      { key: "name", colSpan: 5 },
      { key: "created_at", colSpan: 2 },
      { key: "modified_at", colSpan: 2 },
    ].map(c => ({
      ...c,
      label: $investorFields[c.key].label,
    })),
  )

  let columns = $derived(model === "deal" ? dealColumns : investorColumns)
</script>

{#await dataPromise}
  <div class="m-5">{$_("Loading...")}</div>
{:then data}
  <Table
    {columns}
    items={data}
    colWidthInPx={70}
    rowHeightInPx={70}
    headerHeightInPx={54}
  >
    {#snippet field({ fieldName, obj })}
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
    {/snippet}
  </Table>
{:catch error}
  <div class="m-5">{$_("Error")} {error}</div>
{/await}
