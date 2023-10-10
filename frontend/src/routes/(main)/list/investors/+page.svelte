<script lang="ts">
  import { Client, gql, queryStore } from "@urql/svelte"
  import { _ } from "svelte-i18n"
  import { onMount } from "svelte"

  import { page } from "$app/stores"

  import { dealsQuery } from "$lib/dealQueries"
  import { filters, FilterValues, publicOnly } from "$lib/filters"
  import { formfields, isMobile } from "$lib/stores"
  import type { Deal } from "$lib/types/deal"
  import type { GQLFilter } from "$lib/types/filters"
  import type { Investor } from "$lib/types/investor"

  import { showContextBar, showFilterBar } from "$components/Data/stores"
  import DataContainer from "$components/Data/DataContainer.svelte"
  import DisplayField from "$components/Fields/DisplayField.svelte"
  import Table from "$components/Table/Table.svelte"

  const COLUMNS = [
    "modified_at",
    "id",
    "name",
    "country",
    "classification",
    "deals",
  ] as const

  type ColumnName = (typeof COLUMNS)[number]

  const columnSpanMap: { [key in ColumnName]: number } = {
    modified_at: 2,
    id: 1,
    name: 3,
    country: 4,
    classification: 4,
    deals: 1,
  }

  $: columns = COLUMNS.map(col => col)
  $: labels = COLUMNS.map(col => $formfields.investor[col].label)
  $: spans = COLUMNS.map(col => columnSpanMap[col])

  $: deals = queryStore({
    client: $page.data.urqlClient,
    query: dealsQuery,
    variables: {
      filters: $filters.toGQLFilterArray(),
      subset: $publicOnly ? "PUBLIC" : "ACTIVE",
    },
  })

  let investors: Investor[] = []

  async function getInvestors(s_deals: Deal[], s_filters: FilterValues) {
    if (!$deals) {
      investors = []
      return
    }
    const dealIDs = s_deals.map(d => d.id)
    const tooManyDealsHack = s_deals.length > 2500
    const filters: GQLFilter[] = tooManyDealsHack
      ? []
      : [{ field: "child_deals.id", operation: "IN", value: dealIDs }]
    if (s_filters.investor) filters.push({ field: "id", value: s_filters.investor.id })

    if (s_filters.investor_country_id)
      filters.push({ field: "country_id", value: s_filters.investor_country_id })

    const { error, data } = await ($page.data.urqlClient as Client)
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
        { filters },
      )
      .toPromise()

    if (error || !data) {
      console.error(error)
      return
    }

    investors = data.investors.filter((investor, index, self) => {
      // remove duplicates
      if (self.indexOf(investor) !== index) return false
      // filter for deals
      if (tooManyDealsHack) {
        return investor.deals?.some((d: Deal) => dealIDs.includes(d.id))
      }
      return true
    })
  }

  $: getInvestors($deals?.data?.deals ?? [], $filters)

  onMount(() => {
    showContextBar.set(false)
    showFilterBar.set(!$isMobile)
  })
</script>

<DataContainer>
  <div class="flex h-full">
    <div
      class="h-full min-h-[3px] w-0 flex-none {$showFilterBar
        ? 'md:w-[clamp(220px,20%,300px)]'
        : ''}"
    />

    <div class="flex h-full w-1 grow flex-col px-6 pb-6">
      <div class="flex h-20 items-center text-lg">
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
    <!--    <div-->
    <!--      class="h-full min-h-[3px] flex-none {$showContextBar-->
    <!--        ? 'w-[clamp(220px,20%,300px)]'-->
    <!--        : 'w-0'}"-->
    <!--    />-->
  </div>
</DataContainer>
