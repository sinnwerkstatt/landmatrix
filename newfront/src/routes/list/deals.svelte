<script lang="ts">
  import { queryStore } from "@urql/svelte";
  import { _ } from "svelte-i18n";
  import { page } from "$app/stores";
  import { loading } from "$lib/data";
  import { data_deal_query_gql } from "$lib/deal_queries";
  import { filters, publicOnly } from "$lib/filters";
  import { formfields } from "$lib/stores";
  import { showContextBar, showFilterBar } from "$components/Data";
  import DataContainer from "$components/Data/DataContainer.svelte";
  import FilterCollapse from "$components/Data/FilterCollapse.svelte";
  import DisplayField from "$components/Fields/DisplayField.svelte";
  import Table from "$components/table/Table.svelte";

  let activeColumns = [
    "fully_updated_at",
    "id",
    "country",
    "current_intention_of_investment",
    "operating_company",
  ];

  const allColumnsWithSpan = {
    fully_updated_at: 2,
    deal_size: 2,
    id: 1,
    country: 3,
    current_intention_of_investment: 5,
    current_negotiation_status: 4,
    current_contract_size: 3,
    current_implementation_status: 4,
    intended_size: 2,
    operating_company: 4,
  };

  $: labels = activeColumns.map((col) => $formfields.deal[col].label);
  $: spans = Object.entries(allColumnsWithSpan)
    .filter(([col, _]) => activeColumns.includes(col))
    .map(([_, colSpan]) => colSpan);

  showContextBar.set(false);

  $: deals = queryStore({
    client: $page.stuff.urqlClient,
    query: data_deal_query_gql,
    variables: {
      filters: $filters.toGQLFilterArray(),
      subset: $publicOnly ? "PUBLIC" : "ACTIVE",
    },
  });
  $: loading.set($deals?.fetching ?? false);
</script>

<DataContainer>
  <div class="h-full flex">
    <div
      class="flex-none h-full min-h-[3px] {$showFilterBar
        ? 'w-[clamp(220px,20%,300px)]'
        : 'w-0'}"
    />

    <div class="px-4 bg-stone-100 w-full flex flex-col">
      <div class="h-[4rem] flex items-center pl-2 text-lg">
        {$deals?.data?.deals?.length ?? "—"}
        {$deals?.data?.deals?.length === 1 ? $_("Deal") : $_("Deals")}
      </div>

      <Table
        sortBy="-fully_updated_at"
        items={$deals?.data?.deals ?? []}
        columns={activeColumns}
        {spans}
        {labels}
      >
        <DisplayField
          slot="field"
          let:fieldName
          let:obj
          wrapperClasses="p-1"
          fieldname={fieldName}
          value={obj[fieldName]}
        />
      </Table>
    </div>
    <div
      class="flex-none h-full min-h-[3px] {$showContextBar
        ? 'w-[clamp(220px,20%,300px)]'
        : 'w-0'}"
    />
  </div>

  <div slot="FilterBar">
    <FilterCollapse title={$_("Table columns")}>
      <div class="flex flex-col">
        {#each Object.keys(allColumnsWithSpan) as opt}
          <label>
            <input type="checkbox" bind:group={activeColumns} value={opt} />
            {$_($formfields.deal[opt]?.label)}
          </label>
        {/each}
      </div>
    </FilterCollapse>
  </div>
</DataContainer>
