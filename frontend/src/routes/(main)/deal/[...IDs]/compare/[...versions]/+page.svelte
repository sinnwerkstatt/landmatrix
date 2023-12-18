<script lang="ts">
  import { _ } from "svelte-i18n"

  import { dealSections, subsections } from "$lib/sections"
  import { formfields } from "$lib/stores"

  import DisplayField from "$components/Fields/DisplayField.svelte"

  export let data

  function anyFieldFromSection(subsections) {
    return subsections.some(subsec => anyFieldFromSubSection(subsec))
  }

  function anyFieldFromSubSection(subsec) {
    return subsec.fields.some(f => data.dealdiff.has(f))
  }

  $: labels = {
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
  }

  function hasDifference(dFrom, dTo, field, jfield) {
    if (!dFrom[field] || !dTo[field]) return true
    if (typeof dFrom[field][jfield] == "object") {
      return JSON.stringify(dFrom[field][jfield]) !== JSON.stringify(dTo[field][jfield])
    }
    return dFrom[field][jfield] !== dTo[field][jfield]
  }
</script>

<svelte:head>
  <title>
    {$_("Comparing deal #{dealID}", { values: { dealID: data.dealID } })}
    @{data.versionFrom} - @{data.versionTo}
  </title>
</svelte:head>

<div class="container mx-auto my-12">
  <table
    class="w-full table-fixed border-separate border-spacing-0 text-xs md:text-sm lg:text-base"
  >
    <thead class="sticky top-0 bg-white dark:bg-gray-800">
      <tr class="text-base md:text-lg xl:text-xl">
        <th class="w-1/5 border-t">
          <a href="/deal/{data.dealID}">{$_("Deal")} #{data.dealID}</a>
        </th>
        <th class="w-2/5 border-t">
          <a href="/deal/{data.dealID}/{data.versionFrom}">
            {$_("Version")}
            {data.versionFrom}
          </a>
        </th>
        <th class="w-2/5 border-t">
          <a href="/deal/{data.dealID}/{data.versionTo}">
            {$_("Version")}
            {data.versionTo}
          </a>
        </th>
      </tr>
    </thead>

    <tbody>
      {#each Object.entries($dealSections) as [label, section]}
        {#if anyFieldFromSection(section)}
          <tr class="bg-gray-700">
            <th colspan="3">
              <h2 class="text-white">{labels[label]}</h2>
            </th>
          </tr>
          {#each section as subsec}
            {#if anyFieldFromSubSection(subsec)}
              <tr class="bg-gray-100 dark:bg-gray-600">
                <th colspan="3">
                  <h3>{subsec.name}</h3>
                </th>
              </tr>
              {#each subsec.fields as field}
                {#if data.dealdiff.has(field)}
                  <tr class="odd:bg-gray-50 dark:odd:bg-gray-700">
                    <th>
                      {$formfields.deal[field].label}
                    </th>
                    <td>
                      <DisplayField
                        wrapperClasses="py-2"
                        fieldname={field}
                        value={data.dealFrom[field]}
                      />
                    </td>
                    <td>
                      <DisplayField
                        wrapperClasses="py-2"
                        fieldname={field}
                        value={data.dealTo[field]}
                      />
                    </td>
                  </tr>
                {/if}
              {/each}
            {/if}
          {/each}
        {/if}
      {/each}

      {#if data.locationsdiff}
        <tr class="bg-gray-700">
          <th colspan="3">
            <h2 class="text-white">{$_("Locations")}</h2>
          </th>
        </tr>
        {#each [...data.locationsdiff] as field}
          <tr class="bg-gray-100 dark:bg-gray-600">
            <th colspan="3">
              <h3>{$_("Location")} #{+field + 1}</h3>
            </th>
          </tr>
          {#each subsections.location as jfield}
            {#if hasDifference(data.dealFrom.locations, data.dealTo.locations, field, jfield)}
              <tr class="odd:bg-gray-50 dark:odd:bg-gray-700">
                <th>
                  {$formfields.location[jfield].label}
                </th>
                <td>
                  {#if data.dealFrom.locations[field]}
                    <DisplayField
                      wrapperClasses="py-2"
                      fieldname={jfield}
                      value={data.dealFrom.locations[field][jfield]}
                      model="location"
                    />
                  {/if}
                </td>
                <td>
                  {#if data.dealTo.locations[field]}
                    <DisplayField
                      wrapperClasses="py-2"
                      fieldname={jfield}
                      value={data.dealTo.locations[field][jfield]}
                      model="location"
                    />
                  {/if}
                </td>
              </tr>
            {/if}
          {/each}
        {/each}
      {/if}

      {#if data.datasourcesdiff}
        <tr class="bg-gray-700">
          <th colspan="3">
            <h2 class="text-white">{$_("Data sources")}</h2>
          </th>
        </tr>
        {#each [...data.datasourcesdiff] as field}
          <tr class="bg-gray-100 dark:bg-gray-600">
            <th colspan="3">
              <h3>{$_("Data source")} #{+field + 1}</h3>
            </th>
          </tr>
          {#each subsections.datasource as jfield}
            {#if hasDifference(data.dealFrom.datasources, data.dealTo.datasources, field, jfield)}
              <tr class="odd:bg-gray-50 dark:odd:bg-gray-700">
                <th>
                  {$formfields.datasource[jfield].label}
                </th>
                <td>
                  {#if data.dealFrom.datasources[field]}
                    <DisplayField
                      wrapperClasses="py-2"
                      fieldname={jfield}
                      value={data.dealFrom.datasources[field][jfield]}
                      model="datasource"
                    />
                  {/if}
                </td>
                <td>
                  {#if data.dealTo.datasources[field]}
                    <DisplayField
                      wrapperClasses="py-2"
                      fieldname={jfield}
                      value={data.dealTo.datasources[field][jfield]}
                      model="datasource"
                    />
                  {/if}
                </td>
              </tr>
            {/if}
          {/each}
        {/each}
      {/if}

      {#if data.contractsdiff}
        <tr class="bg-gray-700">
          <th colspan="3">
            <h2 class="text-white">{$_("Contracts")}</h2>
          </th>
        </tr>
        {#each [...data.contractsdiff] as field}
          <tr class="bg-gray-100 dark:bg-gray-600">
            <th colspan="3">
              <h3>{$_("Contract")} #{+field + 1}</h3>
            </th>
          </tr>
          {#each subsections.contract as jfield}
            {#if hasDifference(data.dealFrom.contracts, data.dealTo.contracts, field, jfield)}
              <tr class="odd:bg-gray-50 dark:odd:bg-gray-700">
                <th>
                  {$formfields.contract[jfield].label}
                </th>
                <td>
                  {#if data.dealFrom.contracts[field]}
                    <DisplayField
                      wrapperClasses="py-2"
                      fieldname={jfield}
                      value={data.dealFrom.contracts[field][jfield]}
                      model="contract"
                    />
                  {/if}
                </td>
                <td>
                  {#if data.dealTo.contracts[field]}
                    <DisplayField
                      wrapperClasses="py-2"
                      fieldname={jfield}
                      value={data.dealTo.contracts[field][jfield]}
                      model="contract"
                    />
                  {/if}
                </td>
              </tr>
            {/if}
          {/each}
        {/each}
      {/if}
    </tbody>
  </table>
</div>

<!--TODO: Include in class tag after refactoring component logic-->
<style lang="css">
  table td,
  table th {
    @apply border-b border-r p-2 dark:border-gray-100;
  }

  table th:first-child {
    @apply border-l dark:border-gray-100;
  }

  h2 {
    @apply my-0 text-center text-lg md:text-xl xl:text-2xl;
  }

  h3 {
    @apply my-0 text-center text-sm md:text-base xl:text-lg;
  }
</style>
