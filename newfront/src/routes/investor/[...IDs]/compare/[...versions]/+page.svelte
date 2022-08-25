<script src="+page.ts"></script>
<script lang="ts">
  import { _ } from "svelte-i18n";
  import { investorSections, subsections } from "$lib/sections";
  import { formfields } from "$lib/stores";
  import type { Investor } from "$lib/types/investor";
  import DisplayField from "$components/Fields/DisplayField.svelte";

  // import type { PageData } from "./$types";
  //
  // export let data: PageData;
  export let data: {
    investorID: number;
    versionFrom: number;
    versionTo: number;
    investorFrom: Investor;
    investorTo: Investor;
    investordiff: string[];
    datasourcesdiff: string[] | null;
    involvementsdiff: string[] | null;
  };
  function anyFieldFromSection(subsections) {
    return subsections.some((subsec) => anyFieldFromSubSection(subsec));
  }

  function anyFieldFromSubSection(subsec) {
    return subsec.fields.some((f) => data.investordiff.includes(f));
  }

  const labels = {
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
  };

  function hasDifference(dFrom, dTo, field, jfield) {
    if (!dFrom || !dTo) return true;
    if (!dFrom[field] || !dTo[field]) return true;
    if (typeof dFrom[field][jfield] == "object") {
      return (
        JSON.stringify(dFrom[field][jfield]) !== JSON.stringify(dTo[field][jfield])
      );
    }
    return dFrom[field][jfield] !== dTo[field][jfield];
  }
</script>

<svelte:head>
  <title>
    {$_("Comparing Investor")}
    #{data.investorID} @{data.versionFrom} - @{data.versionTo}
  </title>
</svelte:head>

<table class="mx-4 my-12">
  <thead>
    <tr class="text-2xl">
      <th class="pl-1">
        <a href="/investor/{data.investorID}">{$_("Investor")} #{data.investorID} </a>
      </th>
      <th class="px-4">
        <a href="/investor/{data.investorID}/{data.versionFrom}"
          >{$_("Version")} {data.versionFrom}</a
        >
      </th>
      <th>
        <a href="/investor/{data.investorID}/{data.versionTo}"
          >{$_("Version")} {data.versionTo}</a
        >
      </th>
    </tr>
  </thead>

  <tbody>
    {#each Object.entries(investorSections) as [label, section]}
      {#if anyFieldFromSection(section)}
        <tr>
          <th colspan="3" class="bg-gray-500 py-4">
            <h2 class="text-white my-0 pl-2">{labels[label]}</h2>
          </th>
        </tr>
        {#each section as subsec}
          {#if anyFieldFromSubSection(subsec)}
            <tr>
              <th colspan="3" class="bg-gray-300 py-2">
                <h3 class="text-lg m-0 pl-5">{subsec.name}</h3>
              </th>
            </tr>
            {#each subsec.fields as field}
              {#if data.investordiff.includes(field)}
                <tr class="odd:bg-gray-100">
                  <th class="py-2 pl-8 whitespace-nowrap">
                    {$formfields.investor[field].label}
                  </th>
                  <td>
                    <DisplayField
                      wrapperClasses="px-4 py-2"
                      fieldname={field}
                      value={data.investorFrom[field]}
                      model="investor"
                    />
                  </td>
                  <td>
                    <DisplayField
                      wrapperClasses="py-2"
                      fieldname={field}
                      value={data.investorTo[field]}
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

    {#if data.involvementsdiff}
      <tr class="border-t-[3rem] border-white">
        <th colspan="3" class="bg-gray-500 py-4">
          <h2 class="text-white my-0 pl-2">{$_("Involvements")}</h2>
        </th>
      </tr>
      {#each [...data.involvementsdiff] as field}
        <tr>
          <th colspan="3" class="bg-gray-300 py-2">
            <h3 class="text-lg m-0 pl-5">{$_("Involvement")} #{+field + 1}</h3>
          </th>
        </tr>
        {#each subsections.involvement as jfield}
          {#if hasDifference(data.investorFrom.investors, data.investorTo.investors, field, jfield)}
            <tr class="odd:bg-gray-100">
              <th class="py-2 pl-8 whitespace-nowrap">
                {$formfields.involvement[jfield].label}
              </th>

              <td>
                {#if data.investorFrom.investors?.[field]}
                  <DisplayField
                    wrapperClasses="px-4 py-2"
                    fieldname={jfield}
                    value={data.investorFrom.investors[field][jfield]}
                    model="involvement"
                  />
                {/if}
              </td>
              <td>
                {#if data.investorTo.investors?.[field]}
                  <DisplayField
                    wrapperClasses="py-2"
                    fieldname={jfield}
                    value={data.investorTo.investors[field][jfield]}
                    model="involvement"
                  />
                {/if}
              </td>
            </tr>
          {/if}
        {/each}
      {/each}
    {/if}

    {#if data.datasourcesdiff}
      <tr class="border-t-[3rem] border-white">
        <th colspan="3" class="bg-gray-500 py-4">
          <h2 class="text-white my-0 pl-2">{$_("Data sources")}</h2>
        </th>
      </tr>
      {#each [...data.datasourcesdiff] as field}
        <tr>
          <th colspan="3" class="bg-gray-300 py-2">
            <h3 class="text-lg m-0 pl-5">{$_("Data source")} #{+field + 1}</h3>
          </th>
        </tr>
        {#each subsections.datasource as jfield}
          {#if hasDifference(data.investorFrom.datasources, data.investorTo.datasources, field, jfield)}
            <tr class="odd:bg-gray-100">
              <th class="py-2 pl-8 whitespace-nowrap">
                {$formfields.datasource[jfield].label}
              </th>
              <td>
                {#if data.investorFrom.datasources?.[field]}
                  <DisplayField
                    wrapperClasses="px-4 py-2"
                    fieldname={jfield}
                    value={data.investorFrom.datasources[field][jfield]}
                    model="datasource"
                  />
                {/if}
              </td>
              <td>
                {#if data.investorTo.datasources?.[field]}
                  <DisplayField
                    wrapperClasses="py-2"
                    fieldname={jfield}
                    value={data.investorTo.datasources[field][jfield]}
                    model="datasource"
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
