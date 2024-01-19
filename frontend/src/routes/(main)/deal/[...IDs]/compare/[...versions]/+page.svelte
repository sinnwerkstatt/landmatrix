<script lang="ts">
  import { _ } from "svelte-i18n"

  import { dealFields } from "$lib/fieldLookups"
  import { dealSections } from "$lib/sections"

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
          <a href="/deal/{data.dealID}">{$_("Deal")} #{data.dealID}</a>
        </th>
        <th class="w-2/5 border-t">
          <a href="/deal/{data.dealID}/{data.fromVersion.id}/">
            {$_("Version")}
            {data.fromVersion.id}
          </a>
        </th>
        <th class="w-2/5 border-t">
          <a href="/deal/{data.dealID}/{data.toVersion.id}/">
            {$_("Version")}
            {data.toVersion.id}
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
                      {$dealFields[field].label}
                    </th>
                    <td>
                      <DisplayField
                        fieldname={field}
                        value={data.fromVersion[field]}
                        wrapperClass="py-2"
                      />
                    </td>
                    <td>
                      <DisplayField
                        fieldname={field}
                        value={data.toVersion[field]}
                        wrapperClass="py-2"
                      />
                    </td>
                  </tr>
                {/if}
              {/each}
            {/if}
          {/each}
        {/if}
      {/each}

      <!--      {#if data.locationsdiff}-->
      <!--        <tr class="bg-gray-700">-->
      <!--          <th colspan="3">-->
      <!--            <h2 class="text-white">{$_("Locations")}</h2>-->
      <!--          </th>-->
      <!--        </tr>-->
      <!--        {#each [...data.locationsdiff] as field}-->
      <!--          <tr class="bg-gray-100 dark:bg-gray-600">-->
      <!--            <th colspan="3">-->
      <!--              <h3>{$_("Location")} #{+field + 1}</h3>-->
      <!--            </th>-->
      <!--          </tr>-->
      <!--          {#each subsections.location as jfield}-->
      <!--            {#if hasDifference(data.dealFrom.locations, data.dealTo.locations, field, jfield)}-->
      <!--              <tr class="odd:bg-gray-50 dark:odd:bg-gray-700">-->
      <!--                <th>-->
      <!--                  &lt;!&ndash;{$formfields.location[jfield].label}&ndash;&gt;-->
      <!--                </th>-->
      <!--                <td>-->
      <!--                  {#if data.dealFrom.locations[field]}-->
      <!--                    &lt;!&ndash;                    <DisplayField&ndash;&gt;-->
      <!--                    &lt;!&ndash;                      wrapperClasses="py-2"&ndash;&gt;-->
      <!--                    &lt;!&ndash;                      fieldname={jfield}&ndash;&gt;-->
      <!--                    &lt;!&ndash;                      value={data.dealFrom.locations[field][jfield]}&ndash;&gt;-->
      <!--                    &lt;!&ndash;                      model="location"&ndash;&gt;-->
      <!--                    &lt;!&ndash;                    />&ndash;&gt;-->
      <!--                  {/if}-->
      <!--                </td>-->
      <!--                <td>-->
      <!--                  {#if data.dealTo.locations[field]}-->
      <!--                    &lt;!&ndash;                    <DisplayField&ndash;&gt;-->
      <!--                    &lt;!&ndash;                      wrapperClasses="py-2"&ndash;&gt;-->
      <!--                    &lt;!&ndash;                      fieldname={jfield}&ndash;&gt;-->
      <!--                    &lt;!&ndash;                      value={data.dealTo.locations[field][jfield]}&ndash;&gt;-->
      <!--                    &lt;!&ndash;                      model="location"&ndash;&gt;-->
      <!--                    &lt;!&ndash;                    />&ndash;&gt;-->
      <!--                  {/if}-->
      <!--                </td>-->
      <!--              </tr>-->
      <!--            {/if}-->
      <!--          {/each}-->
      <!--        {/each}-->
      <!--      {/if}-->

      <!--{JSON.stringify(data.datasourcesdiff)}-->
      <!--{#if data.datasourcesdiff}-->
      <!--  <tr class="bg-gray-700">-->
      <!--    <th colspan="3">-->
      <!--      <h2 class="text-white">{$_("Data sources")}</h2>-->
      <!--    </th>-->
      <!--  </tr>-->
      <!--  {#each [...data.datasourcesdiff] as field}-->
      <!--    <tr class="bg-gray-100 dark:bg-gray-600">-->
      <!--      <th colspan="3">-->
      <!--        <h3>{$_("Data source")} #{+field + 1}</h3>-->
      <!--      </th>-->
      <!--    </tr>-->
      <!--    {#each subsections.datasource as jfield}-->
      <!--      {#if hasDifference(data.fromVersion.datasources, data.toVersion.datasources, field, jfield)}-->
      <!--        <tr class="odd:bg-gray-50 dark:odd:bg-gray-700">-->
      <!--          <th>-->
      <!--            {jfield}-->
      <!--            {field}-->
      <!--            &lt;!&ndash;{$dealFields[`datasource.${field}`].label}&ndash;&gt;-->
      <!--          </th>-->
      <!--          <td>-->
      <!--            &lt;!&ndash;{#if data.fromVersion.datasources[field]}&ndash;&gt;-->
      <!--            &lt;!&ndash;  &lt;!&ndash;                    <DisplayField&ndash;&gt;&ndash;&gt;-->
      <!--            &lt;!&ndash;  &lt;!&ndash;                      fieldname={jfield}&ndash;&gt;&ndash;&gt;-->
      <!--            &lt;!&ndash;  &lt;!&ndash;                      value={data.fromVersion.datasources[field][jfield]}&ndash;&gt;&ndash;&gt;-->
      <!--            &lt;!&ndash;  &lt;!&ndash;                      wrapperClass="py-2"&ndash;&gt;&ndash;&gt;-->
      <!--            &lt;!&ndash;  &lt;!&ndash;                    />&ndash;&gt;&ndash;&gt;-->
      <!--            &lt;!&ndash;  &lt;!&ndash;                                        <DisplayField&ndash;&gt;&ndash;&gt;-->
      <!--            &lt;!&ndash;  &lt;!&ndash;                                          wrapperClass="py-2"&ndash;&gt;&ndash;&gt;-->
      <!--            &lt;!&ndash;  &lt;!&ndash;                                          fieldname={jfield}&ndash;&gt;&ndash;&gt;-->
      <!--            &lt;!&ndash;  &lt;!&ndash;                                          value={data.dealFrom.datasources[field][jfield]}&ndash;&gt;&ndash;&gt;-->
      <!--            &lt;!&ndash;  &lt;!&ndash;                                          model="datasource"&ndash;&gt;&ndash;&gt;-->
      <!--            &lt;!&ndash;  &lt;!&ndash;                                        />&ndash;&gt;&ndash;&gt;-->
      <!--            &lt;!&ndash;{/if}&ndash;&gt;-->
      <!--          </td>-->
      <!--          <td>-->
      <!--            &lt;!&ndash;{#if data.dealTo.datasources[field]}&ndash;&gt;-->
      <!--            &lt;!&ndash;  &lt;!&ndash;                    <DisplayField&ndash;&gt;&ndash;&gt;-->
      <!--            &lt;!&ndash;  &lt;!&ndash;                      wrapperClasses="py-2"&ndash;&gt;&ndash;&gt;-->
      <!--            &lt;!&ndash;  &lt;!&ndash;                      fieldname={jfield}&ndash;&gt;&ndash;&gt;-->
      <!--            &lt;!&ndash;  &lt;!&ndash;                      value={data.dealTo.datasources[field][jfield]}&ndash;&gt;&ndash;&gt;-->
      <!--            &lt;!&ndash;  &lt;!&ndash;                      model="datasource"&ndash;&gt;&ndash;&gt;-->
      <!--            &lt;!&ndash;  &lt;!&ndash;                    />&ndash;&gt;&ndash;&gt;-->
      <!--            &lt;!&ndash;{/if}&ndash;&gt;-->
      <!--          </td>-->
      <!--        </tr>-->
      <!--      {/if}-->
      <!--    {/each}-->
      <!--  {/each}-->
      <!--{/if}-->

      <!--      {#if data.contractsdiff}-->
      <!--        <tr class="bg-gray-700">-->
      <!--          <th colspan="3">-->
      <!--            <h2 class="text-white">{$_("Contracts")}</h2>-->
      <!--          </th>-->
      <!--        </tr>-->
      <!--        {#each [...data.contractsdiff] as field}-->
      <!--          <tr class="bg-gray-100 dark:bg-gray-600">-->
      <!--            <th colspan="3">-->
      <!--              <h3>{$_("Contract")} #{+field + 1}</h3>-->
      <!--            </th>-->
      <!--          </tr>-->
      <!--          {#each subsections.contract as jfield}-->
      <!--            {#if hasDifference(data.dealFrom.contracts, data.dealTo.contracts, field, jfield)}-->
      <!--              <tr class="odd:bg-gray-50 dark:odd:bg-gray-700">-->
      <!--                <th>-->
      <!--                  &lt;!&ndash;{$formfields.contract[jfield].label}&ndash;&gt;-->
      <!--                </th>-->
      <!--                <td>-->
      <!--                  {#if data.dealFrom.contracts[field]}-->
      <!--                    &lt;!&ndash;                    <DisplayField&ndash;&gt;-->
      <!--                    &lt;!&ndash;                      wrapperClasses="py-2"&ndash;&gt;-->
      <!--                    &lt;!&ndash;                      fieldname={jfield}&ndash;&gt;-->
      <!--                    &lt;!&ndash;                      value={data.dealFrom.contracts[field][jfield]}&ndash;&gt;-->
      <!--                    &lt;!&ndash;                      model="contract"&ndash;&gt;-->
      <!--                    &lt;!&ndash;                    />&ndash;&gt;-->
      <!--                  {/if}-->
      <!--                </td>-->
      <!--                <td>-->
      <!--                  {#if data.dealTo.contracts[field]}-->
      <!--                    &lt;!&ndash;                    <DisplayField&ndash;&gt;-->
      <!--                    &lt;!&ndash;                      wrapperClasses="py-2"&ndash;&gt;-->
      <!--                    &lt;!&ndash;                      fieldname={jfield}&ndash;&gt;-->
      <!--                    &lt;!&ndash;                      value={data.dealTo.contracts[field][jfield]}&ndash;&gt;-->
      <!--                    &lt;!&ndash;                      model="contract"&ndash;&gt;-->
      <!--                    &lt;!&ndash;                    />&ndash;&gt;-->
      <!--                  {/if}-->
      <!--                </td>-->
      <!--              </tr>-->
      <!--            {/if}-->
      <!--          {/each}-->
      <!--        {/each}-->
      <!--      {/if}-->
    </tbody>
  </table>
</div>

<!--TODO: Include in class tag after refactoring component logic-->
<style lang="postcss">
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
