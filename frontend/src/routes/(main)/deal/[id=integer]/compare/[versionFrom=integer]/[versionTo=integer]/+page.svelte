<script lang="ts">
  import { _ } from "svelte-i18n"

  import { dealFields } from "$lib/fieldLookups"
  import { dealSectionsLG } from "$lib/sections"
  import type { Area, Contract, DataSource, Location2 } from "$lib/types/data"

  import CompareSubmodelDiffBlock from "$components/CompareSubmodelDiffBlock.svelte"
  import DisplayField from "$components/Fields/DisplayField.svelte"

  let { data } = $props()

  let labels: { [sectionKey: string]: string } = $derived({
    general_info: $_("General info"),
    employment: $_("Employment"),
    investor_info: $_("Investor info"),
    local_communities: $_("Local communities / indigenous peoples"),
    former_use: $_("Former use"),
    produce_info: $_("Produce info"),
    water: $_("Water"),
    gender_related_info: $_("Gender-related info"),
    overall_comment: $_("Overall comment"),
    meta: $_("Meta"),
  })

  const cleanArea = (area: Area) => ({
    ...area,
    id: undefined,
    location: undefined,
  })

  const cleanLocation = (location: Location2) => ({
    ...location,
    id: undefined,
    dealversion: undefined,
    areas: location.areas.map(cleanArea),
  })

  const cleanDataSource = (dataSource: DataSource) => ({
    ...dataSource,
    id: undefined,
    dealversion: undefined,
  })

  const cleanContract = (contract: Contract) => ({
    ...contract,
    id: undefined,
    dealversion: undefined,
  })

  const fromLocs = data.fromVersion.locations.map(cleanLocation)
  const toLocs = data.toVersion.locations.map(cleanLocation)

  const fromDSs = data.fromVersion.datasources.map(cleanDataSource)
  const toDSs = data.toVersion.datasources.map(cleanDataSource)

  const fromCons = data.fromVersion.contracts.map(cleanContract)
  const toCons = data.toVersion.contracts.map(cleanContract)
</script>

<svelte:head>
  <title>
    {$_("Comparing deal #{dealId}", {
      values: { dealId: data.dealId },
    })}
    @{data.fromVersion.id} - @{data.toVersion.id}
  </title>
</svelte:head>

<div class="container mx-auto my-12">
  <table
    class="w-full table-fixed border-separate border-spacing-0 text-xs md:text-sm lg:text-base"
  >
    <thead class="sticky top-0 bg-white dark:bg-gray-800">
      <tr class="text-base md:text-lg xl:text-xl">
        <th class="w-1/5 border-t">
          <a href="/deal/{data.dealId}/">
            {$_("Deal")} #{data.dealId}
          </a>
        </th>
        <th class="w-2/5 border-t">
          <a href="/deal/{data.dealId}/{data.fromVersion.id}/">
            {$_("Version")}
            {data.fromVersion.id}
          </a>
        </th>
        <th class="w-2/5 border-t">
          <a href="/deal/{data.dealId}/{data.toVersion.id}/">
            {$_("Version")}
            {data.toVersion.id}
          </a>
        </th>
      </tr>
    </thead>

    <tbody>
      {#each Object.entries($dealSectionsLG) as [label, section]}
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
            {#if data.dealdiff.has(field)}
              <tr class="🍌">
                <th>
                  {$dealFields[field]?.label ?? field}
                </th>
                <td>
                  <DisplayField
                    fieldname={field}
                    value={data.fromVersion[field]}
                    wrapperClass="py-2"
                    valueClass=""
                  />
                </td>
                <td>
                  <DisplayField
                    fieldname={field}
                    value={data.toVersion[field]}
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
        fromObjs={fromLocs}
        heading={$_("Locations")}
        label={$_("Location")}
        lookupString="location"
        toObjs={toLocs}
      />

      <CompareSubmodelDiffBlock
        fromObjs={fromDSs}
        heading={$_("Data sources")}
        label={$_("Data source")}
        lookupString="datasource"
        toObjs={toDSs}
      />

      <CompareSubmodelDiffBlock
        fromObjs={fromCons}
        heading={$_("Contracts")}
        label={$_("Contract")}
        lookupString="contract"
        toObjs={toCons}
      />
    </tbody>
  </table>
</div>

<!--TODO Later: Include in class tag after refactoring component logic-->
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
