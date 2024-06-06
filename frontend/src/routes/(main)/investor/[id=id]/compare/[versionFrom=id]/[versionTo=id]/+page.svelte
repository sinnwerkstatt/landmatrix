<script lang="ts">
  import { _ } from "svelte-i18n"

  import { investorFields } from "$lib/fieldLookups"

  import CompareSubmodelDiffBlock from "$components/CompareSubmodelDiffBlock.svelte"
  import DisplayField from "$components/Fields/DisplayField.svelte"

  export let data

  $: labels = { general_info: $_("General info") }

  $: investorSections = {
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
  }

  $: fromDSs = data.fromVersion.datasources.map(l => ({
    ...l,
    id: undefined,
    investorversion: undefined,
  }))
  $: toDSs = data.toVersion.datasources.map(l => ({
    ...l,
    id: undefined,
    investorversion: undefined,
  }))

  $: fromInvos = data.fromVersion.involvements_snapshot.map(l => ({
    ...l,
    id: undefined,
    parent_investor_id: undefined,
    child_investor_id: undefined,
  }))
  $: toInvos = data.toVersion.involvements_snapshot.map(l => ({
    ...l,
    id: undefined,
    parent_investor_id: undefined,
    child_investor_id: undefined,
  }))
</script>

<svelte:head>
  <title>
    {$_("Comparing investor #{investorID}", {
      values: { investorID: data.investorID },
    })}
    @{data.fromVersion.id} - @{data.toVersion.id}
  </title>
</svelte:head>

<table class="container mx-4 my-12">
  <thead>
    <tr class="text-2xl">
      <th class="pl-1">
        <a href="/investor/{data.investorID}" class="investor">
          {$_("Investor")} #{data.investorID}
        </a>
      </th>
      <th class="px-4">
        <a href="/investor/{data.investorID}/{data.fromVersion.id}/" class="investor">
          {$_("Version")}
          {data.fromVersion.id}
        </a>
      </th>
      <th>
        <a href="/investor/{data.investorID}/{data.toVersion.id}/" class="investor">
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
        <tr class="🍏 hidden bg-gray-100 py-2 dark:bg-gray-600 [&:has(+.🍌)]:table-row">
          <th colspan="3">
            <h3>{subsec.name}</h3>
          </th>
        </tr>
        {#each subsec.fields as field}
          {#if data.investordiff.has(field)}
            <tr class="🍌 odd:bg-gray-50 dark:odd:bg-gray-700">
              <th class="whitespace-nowrap py-2 pl-8">
                {$investorFields[field].label}
              </th>
              <td>
                <DisplayField
                  wrapperClass="px-4 py-2"
                  fieldname={field}
                  value={data.fromVersion[field]}
                  model="investor"
                />
              </td>
              <td>
                <DisplayField
                  wrapperClass="py-2"
                  fieldname={field}
                  value={data.toVersion[field]}
                  model="investor"
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
    />

    <CompareSubmodelDiffBlock
      fromObjs={fromInvos}
      heading={$_("Involvements")}
      label={$_("Involvement")}
      lookupString="involvement"
      toObjs={toInvos}
      useInvoID
    />
  </tbody>
</table>

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
