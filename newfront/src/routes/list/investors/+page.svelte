<script lang="ts">
  import { Client, gql, queryStore } from "@urql/svelte";
  import { _ } from "svelte-i18n";
  import { page } from "$app/stores";
  import { data_deal_query_gql } from "$lib/deal_queries";
  import { filters, FilterValues, publicOnly } from "$lib/filters";
  import { formfields } from "$lib/stores";
  import type { Deal } from "$lib/types/deal";
  import type { GQLFilter } from "$lib/types/filters";
  import type { Investor } from "$lib/types/investor";
  import { showContextBar, showFilterBar } from "$components/Data";
  import DataContainer from "$components/Data/DataContainer.svelte";
  import DisplayField from "$components/Fields/DisplayField.svelte";
  import Table from "$components/table/Table.svelte";

  showContextBar.set(false);

  const allColumnsWithSpan = {
    modified_at: 2,
    id: 1,
    name: 3,
    country: 3,
    classification: 4,
    deals: 1,
  };

  $: columns = Object.keys(allColumnsWithSpan);
  $: labels = columns.map((col) => $formfields.investor[col].label);
  $: spans = Object.entries(allColumnsWithSpan).map(([_, colSpan]) => colSpan);

  $: deals = queryStore({
    client: $page.data.urqlClient,
    query: data_deal_query_gql,
    variables: {
      filters: $filters.toGQLFilterArray(),
      subset: $publicOnly ? "PUBLIC" : "ACTIVE",
    },
  });

  let investors: Investor[] = [];

  async function getInvestors(s_deals: Deal[], s_filters: FilterValues) {
    if (!$deals) {
      investors = [];
      return;
    }
    const dealIDs = s_deals.map((d) => d.id);
    const tooManyDealsHack = s_deals.length > 2500;
    const filters: GQLFilter[] = tooManyDealsHack
      ? []
      : [{ field: "child_deals.id", operation: "IN", value: dealIDs }];
    if (s_filters.investor) filters.push({ field: "id", value: s_filters.investor.id });

    if (s_filters.investor_country_id)
      filters.push({ field: "country_id", value: s_filters.investor_country_id });

    const { data } = await ($page.data.urqlClient as Client)
      .query<{ investors: Investor[] }>(
        gql`
          query Investors($filters: [Filter]) {
            investors(limit: 0, filters: $filters) {
              id
              name
              country {
                id
                name
              }
              classification
              homepage
              opencorporates
              comment
              deals {
                id
              }
              status
              draft_status
              created_at
              modified_at
              is_actually_unknown
            }
          }
        `,
        { filters }
      )
      .toPromise();
    if (!data?.investors) {
      console.error("could not grab investors");
      return;
    }

    investors = data.investors.filter((investor, index, self) => {
      // remove duplicates
      if (self.indexOf(investor) !== index) return false;
      // filter for deals
      if (tooManyDealsHack) {
        return investor.deals?.some((d: Deal) => dealIDs.includes(d.id));
      }
      return true;
    });
  }

  $: getInvestors($deals?.data?.deals ?? [], $filters);
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
        {investors?.length ?? "—"}
        {investors?.length === 1 ? $_("Investor") : $_("Investors")}
      </div>

      <Table sortBy="-modified_at" items={investors} {columns} {spans} {labels}>
        <DisplayField
          slot="field"
          let:fieldName
          let:obj
          model="investor"
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
</DataContainer>
