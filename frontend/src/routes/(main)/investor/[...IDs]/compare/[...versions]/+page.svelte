<script lang="ts">
  import { _ } from "svelte-i18n"

  import { investorFields } from "$lib/fieldLookups"
  import { investorSections } from "$lib/sections"

  import TextField from "$components/Fields/Display2/TextField.svelte"
  import DisplayField from "$components/Fields/DisplayField.svelte"

  export let data

  function anyFieldFromSection(subsections) {
    return subsections.some(subsec => anyFieldFromSubSection(subsec))
  }

  function anyFieldFromSubSection(subsec) {
    return subsec.fields.some(f => data.investordiff.has(f))
  }

  $: labels = { general_info: $_("General info") }

  function hasDifference(dFrom, dTo, field, jfield) {
    if (!dFrom || !dTo) return true
    if (!dFrom[field] || !dTo[field]) return true
    if (typeof dFrom[field][jfield] == "object") {
      return JSON.stringify(dFrom[field][jfield]) !== JSON.stringify(dTo[field][jfield])
    }
    return dFrom[field][jfield] !== dTo[field][jfield]
  }
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
        <a href="/investor/{data.investorID}">{$_("Investor")} #{data.investorID}</a>
      </th>
      <th class="px-4">
        <a href="/investor/{data.investorID}/{data.fromVersion.id}">
          {$_("Version")}
          {data.fromVersion.id}
        </a>
      </th>
      <th>
        <a href="/investor/{data.investorID}/{data.toVersion.id}">
          {$_("Version")}
          {data.toVersion.id}
        </a>
      </th>
    </tr>
  </thead>
  <!--  "name", "country", "classification", "homepage", "opencorporates", "comment",-->
  <tbody>
    <tr>
      <td>Name</td>
      <td>
        <TextField value={data.fromVersion.name} />
      </td>
      <td>
        <TextField value={data.toVersion.name} />
      </td>
    </tr>
    {#each Object.entries($investorSections) as [label, section]}
      {#if anyFieldFromSection(section)}
        <tr>
          <th colspan="3" class="bg-gray-700 py-4">
            <h2 class="my-0 pl-2 text-white">{labels[label]}</h2>
          </th>
        </tr>
        {#each section as subsec}
          {#if anyFieldFromSubSection(subsec)}
            <tr>
              <th colspan="3" class="bg-gray-100 py-2 dark:bg-gray-600">
                <h3 class="m-0 pl-5 text-lg">{subsec.name}</h3>
              </th>
            </tr>
            {#each subsec.fields as field}
              {#if data.investordiff.has(field)}
                <tr class="odd:bg-gray-50 dark:odd:bg-gray-700">
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
          {/if}
        {/each}
      {/if}
    {/each}

    <!--{#if data.involvementsdiff}-->
    <!--  <tr class="border-t-[3rem] border-white dark:border-gray-800">-->
    <!--    <th colspan="3" class="bg-gray-700 py-4">-->
    <!--      <h2 class="my-0 pl-2 text-white">{$_("Involvements")}</h2>-->
    <!--    </th>-->
    <!--  </tr>-->
    <!--  {#each [...data.involvementsdiff] as field}-->
    <!--    <tr>-->
    <!--      <th colspan="3" class="bg-gray-100 py-2 dark:bg-gray-600">-->
    <!--        <h3 class="m-0 pl-5 text-lg">{$_("Involvement")} #{+field + 1}</h3>-->
    <!--      </th>-->
    <!--    </tr>-->
    <!--    {#each subsections.involvement as jfield}-->
    <!--      {#if hasDifference(data.fromVersion.investors, data.toVersion.investors, field, jfield)}-->
    <!--        <tr class="odd:bg-gray-50 dark:odd:bg-gray-700">-->
    <!--          <th class="whitespace-nowrap py-2 pl-8">-->
    <!--            &lt;!&ndash;{$formfields.involvement[jfield].label}&ndash;&gt;-->
    <!--          </th>-->

    <!--          <td>-->
    <!--            {#if data.fromVersion.investors?.[field]}-->
    <!--              &lt;!&ndash;                  <DisplayField&ndash;&gt;-->
    <!--              &lt;!&ndash;                    wrapperClasses="px-4 py-2"&ndash;&gt;-->
    <!--              &lt;!&ndash;                    fieldname={jfield}&ndash;&gt;-->
    <!--              &lt;!&ndash;                    value={data.fromVersion.investors[field][jfield]}&ndash;&gt;-->
    <!--              &lt;!&ndash;                    model="involvement"&ndash;&gt;-->
    <!--              &lt;!&ndash;                  />&ndash;&gt;-->
    <!--            {/if}-->
    <!--          </td>-->
    <!--          <td>-->
    <!--            {#if data.toVersion.investors?.[field]}-->
    <!--              &lt;!&ndash;                  <DisplayField&ndash;&gt;-->
    <!--              &lt;!&ndash;                    wrapperClasses="py-2"&ndash;&gt;-->
    <!--              &lt;!&ndash;                    fieldname={jfield}&ndash;&gt;-->
    <!--              &lt;!&ndash;                    value={data.toVersion.investors[field][jfield]}&ndash;&gt;-->
    <!--              &lt;!&ndash;                    model="involvement"&ndash;&gt;-->
    <!--              &lt;!&ndash;                  />&ndash;&gt;-->
    <!--            {/if}-->
    <!--          </td>-->
    <!--        </tr>-->
    <!--      {/if}-->
    <!--    {/each}-->
    <!--  {/each}-->
    <!--{/if}-->

    <!--{#if data.datasourcesdiff}-->
    <!--  <tr class="border-t-[3rem] border-white dark:border-gray-800">-->
    <!--    <th colspan="3" class="bg-gray-700 py-4">-->
    <!--      <h2 class="my-0 pl-2 text-white">{$_("Data sources")}</h2>-->
    <!--    </th>-->
    <!--  </tr>-->
    <!--  {#each [...data.datasourcesdiff] as field}-->
    <!--    <tr>-->
    <!--      <th colspan="3" class="bg-gray-100 py-2 dark:bg-gray-600">-->
    <!--        <h3 class="m-0 pl-5 text-lg">{$_("Data source")} #{+field + 1}</h3>-->
    <!--      </th>-->
    <!--    </tr>-->
    <!--    {#each subsections.datasource as jfield}-->
    <!--      {#if hasDifference(data.fromVersion.datasources, data.toVersion.datasources, field, jfield)}-->
    <!--        <tr class="odd:bg-gray-50 dark:odd:bg-gray-700">-->
    <!--          <th class="whitespace-nowrap py-2 pl-8">-->
    <!--            {$formfields.datasource[jfield].label}-->
    <!--          </th>-->
    <!--          <td>-->
    <!--            {#if data.fromVersion.datasources?.[field]}-->
    <!--              &lt;!&ndash;                  <DisplayField&ndash;&gt;-->
    <!--              &lt;!&ndash;                    wrapperClasses="px-4 py-2"&ndash;&gt;-->
    <!--              &lt;!&ndash;                    fieldname={jfield}&ndash;&gt;-->
    <!--              &lt;!&ndash;                    value={data.fromVersion.datasources[field][jfield]}&ndash;&gt;-->
    <!--              &lt;!&ndash;                    model="datasource"&ndash;&gt;-->
    <!--              &lt;!&ndash;                  />&ndash;&gt;-->
    <!--            {/if}-->
    <!--          </td>-->
    <!--          <td>-->
    <!--            {#if data.toVersion.datasources?.[field]}-->
    <!--              &lt;!&ndash;                  <DisplayField&ndash;&gt;-->
    <!--              &lt;!&ndash;                    wrapperClasses="py-2"&ndash;&gt;-->
    <!--              &lt;!&ndash;                    fieldname={jfield}&ndash;&gt;-->
    <!--              &lt;!&ndash;                    value={data.toVersion.datasources[field][jfield]}&ndash;&gt;-->
    <!--              &lt;!&ndash;                    model="datasource"&ndash;&gt;-->
    <!--              &lt;!&ndash;                  />&ndash;&gt;-->
    <!--            {/if}-->
    <!--          </td>-->
    <!--        </tr>-->
    <!--      {/if}-->
    <!--    {/each}-->
    <!--  {/each}-->
    <!--{/if}-->
  </tbody>
</table>
