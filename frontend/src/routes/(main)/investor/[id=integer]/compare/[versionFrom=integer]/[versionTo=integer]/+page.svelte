<script lang="ts">
  import { _ } from "svelte-i18n"

  import { investorFields } from "$lib/fieldLookups"
  import type { DataSource, Involvement } from "$lib/types/data"

  import CompareSubmodelDiffBlock from "$components/CompareSubmodelDiffBlock.svelte"
  import DisplayField from "$components/Fields/DisplayField.svelte"

  let { data } = $props()

  let labels = $derived({ general_info: $_("General info") })

  let investorSections = $derived({
    general_info: [
      {
        name: $_("General info"),
        fields: [
          "name",
          "country",
          "classification",
          "homepage",
          "opencorporates",
          "comment",
        ],
      },
    ],
  })

  const cleanDataSource = (dataSource: DataSource) => ({
    ...dataSource,
    id: undefined,
    investorversion: undefined,
  })
  const cleanInvolvement = (involvement: Involvement) => ({
    ...involvement,
    id: undefined,
    child_investor_id: undefined,
  })

  let fromDSs = $derived(data.fromVersion.datasources.map(cleanDataSource))
  let toDSs = $derived(data.toVersion.datasources.map(cleanDataSource))

  let fromInvos = $derived(data.fromVersion.involvements_snapshot.map(cleanInvolvement))
  let toInvos = $derived(data.toVersion.involvements_snapshot.map(cleanInvolvement))
</script>

<svelte:head>
  <title>
    {$_("Comparing investor #{investorId}", {
      values: { investorId: data.investorId },
    })}
    @{data.fromVersion.id} - @{data.toVersion.id}
  </title>
</svelte:head>

<div class="container mx-auto my-6 lg:my-12">
  <table
    class="w-full table-fixed border-separate border-spacing-0 text-xs md:text-sm lg:text-base"
  >
    <thead class="sticky top-0 bg-white dark:bg-gray-800">
      <tr class="text-base md:text-lg xl:text-xl">
        <th class="w-1/5 border-t">
          <a href="/investor/{data.investorId}/" class="investor">
            {$_("Investor")} #{data.investorId}
          </a>
        </th>
        <th class="w-2/5 border-t">
          <a href="/investor/{data.investorId}/{data.fromVersion.id}/" class="investor">
            {$_("Version")}
            {data.fromVersion.id}
          </a>
        </th>
        <th class="w-2/5 border-t">
          <a href="/investor/{data.investorId}/{data.toVersion.id}/" class="investor">
            {$_("Version")}
            {data.toVersion.id}
          </a>
        </th>
      </tr>
    </thead>

    <tbody>
      {#each Object.entries(investorSections) as [label, section]}
        <tr class="hidden bg-gray-700 [&:has(+.🍏+.🍌)]:table-row">
          <th colspan="3">
            <h2>{labels[label]}</h2>
          </th>
        </tr>
        {#each section as subsec}
          <tr class="🍏 hidden bg-gray-100 dark:bg-gray-600 [&:has(+.🍌)]:table-row">
            <th colspan="3">
              <h3>{subsec.name}</h3>
            </th>
          </tr>
          {#each subsec.fields as field}
            {#if data.investordiff.has(field)}
              <tr class="🍌">
                <th>
                  {$investorFields[field]?.label ?? field}
                </th>
                <td>
                  <DisplayField
                    fieldname={field}
                    value={data.fromVersion[field]}
                    model="investor"
                    wrapperClass="py-2"
                    valueClass=""
                  />
                </td>
                <td>
                  <DisplayField
                    fieldname={field}
                    value={data.toVersion[field]}
                    model="investor"
                    wrapperClass="py-2"
                    valueClass=""
                  />
                </td>
              </tr>
            {/if}
          {/each}
        {/each}
      {/each}

      <CompareSubmodelDiffBlock
        fromObjs={fromDSs}
        heading={$_("Data sources")}
        label={$_("Data source")}
        lookupString="datasource"
        toObjs={toDSs}
        model="investor"
      />

      <CompareSubmodelDiffBlock
        fromObjs={fromInvos}
        heading={$_("Involvements")}
        label={$_("Involvement")}
        lookupString="involvement"
        toObjs={toInvos}
        model="investor"
      />
    </tbody>
  </table>
</div>

<style lang="postcss">
  table td,
  table th {
    @apply border-b border-r p-2 dark:border-gray-100;
  }

  table th:first-child {
    @apply border-l dark:border-gray-100;
  }

  h2 {
    @apply my-0 text-center text-lg text-white md:text-xl xl:text-2xl;
  }

  h3 {
    @apply my-0 text-center text-sm md:text-base xl:text-lg;
  }
</style>
