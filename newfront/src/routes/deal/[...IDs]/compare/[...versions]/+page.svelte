<script lang="ts">
  import { _ } from "svelte-i18n";
  import { dealSections, subsections } from "$lib/sections";
  import { formfields } from "$lib/stores";
  import type { Deal } from "$lib/types/deal";
  import DisplayField from "$components/Fields/DisplayField.svelte";

  // import type { PageData } from "./$types";
  //
  // export let data: PageData;
  export let data: {
    dealID: number;
    versionFrom: number;
    versionTo: number;
    dealFrom: Deal;
    dealTo: Deal;
    dealdiff: string[];
    locationsdiff: string[] | null;
    datasourcesdiff: string[] | null;
    contractsdiff: string[] | null;
  };
  function anyFieldFromSection(subsections) {
    return subsections.some((subsec) => anyFieldFromSubSection(subsec));
  }
  function anyFieldFromSubSection(subsec) {
    return subsec.fields.some((f) => data.dealdiff.includes(f));
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
    {$_("Comparing Deal")}
    #{data.dealID} @{data.versionFrom} - @{data.versionTo}
  </title>
</svelte:head>

<table class="mx-4 my-12">
  <thead>
    <tr class="text-2xl">
      <th class="pl-1">
        <a href="/deal/{data.dealID}">{$_("Deal")} #{data.dealID} </a>
      </th>
      <th class="px-4">
        <a href="/deal/{data.dealID}/{data.versionFrom}"
          >{$_("Version")} {data.versionFrom}</a
        >
      </th>
      <th>
        <a href="/deal/{data.dealID}/{data.versionTo}"
          >{$_("Version")} {data.versionTo}</a
        ></th
      >
    </tr>
  </thead>

  <tbody>
    {#each Object.entries(dealSections) as [label, section]}
      {#if anyFieldFromSection(section)}
        <tr>
          <th colspan="3" class="bg-gray-500 py-4">
            <h2 class="my-0 pl-2 text-white">{labels[label]}</h2>
          </th>
        </tr>
        {#each section as subsec}
          {#if anyFieldFromSubSection(subsec)}
            <tr>
              <th colspan="3" class="bg-gray-300 py-2">
                <h3 class="m-0 pl-5 text-lg">{subsec.name}</h3>
              </th>
            </tr>
            {#each subsec.fields as field}
              {#if data.dealdiff.includes(field)}
                <tr class="odd:bg-gray-100">
                  <th class="whitespace-nowrap py-2 pl-8">
                    {$formfields.deal[field].label}
                  </th>
                  <td>
                    <DisplayField
                      wrapperClasses="px-4 py-2"
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
      <tr class="border-t-[3rem] border-white">
        <th colspan="3" class="bg-gray-500 py-4">
          <h2 class="my-0 pl-2 text-white">{$_("Locations")}</h2>
        </th>
      </tr>
      {#each [...data.locationsdiff] as field}
        <tr>
          <th colspan="3" class="bg-gray-300 py-2">
            <h3 class="m-0 pl-5 text-lg">{$_("Location")} #{+field + 1}</h3>
          </th>
        </tr>
        {#each subsections.location as jfield}
          {#if hasDifference(data.dealFrom.locations, data.dealTo.locations, field, jfield)}
            <tr class="odd:bg-gray-100">
              <th class="whitespace-nowrap py-2 pl-8">
                {$formfields.location[jfield].label}
              </th>
              <td>
                {#if data.dealFrom.locations[field]}
                  <DisplayField
                    wrapperClasses="px-4 py-2"
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
      <tr class="border-t-[3rem] border-white">
        <th colspan="3" class="bg-gray-500 py-4">
          <h2 class="my-0 pl-2 text-white">{$_("Data sources")}</h2>
        </th>
      </tr>
      {#each [...data.datasourcesdiff] as field}
        <tr>
          <th colspan="3" class="bg-gray-300 py-2">
            <h3 class="m-0 pl-5 text-lg">{$_("Data source")} #{+field + 1}</h3>
          </th>
        </tr>
        {#each subsections.datasource as jfield}
          {#if hasDifference(data.dealFrom.datasources, data.dealTo.datasources, field, jfield)}
            <tr class="odd:bg-gray-100">
              <th class="whitespace-nowrap py-2 pl-8">
                {$formfields.datasource[jfield].label}
              </th>
              <td>
                {#if data.dealFrom.datasources[field]}
                  <DisplayField
                    wrapperClasses="px-4 py-2"
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
      <tr class="border-t-[3rem] border-white">
        <th colspan="3" class="bg-gray-500 py-4">
          <h2 class="my-0 pl-2 text-white">{$_("Contracts")}</h2>
        </th>
      </tr>
      {#each [...data.contractsdiff] as field}
        <tr>
          <th colspan="3" class="bg-gray-300 py-2">
            <h3 class="m-0 pl-5 text-lg">{$_("Contract")} #{+field + 1}</h3>
          </th>
        </tr>
        {#each subsections.contract as jfield}
          {#if hasDifference(data.dealFrom.contracts, data.dealTo.contracts, field, jfield)}
            <tr class="odd:bg-gray-100">
              <th class="whitespace-nowrap py-2 pl-8">
                {$formfields.contract[jfield].label}
              </th>
              <td>
                {#if data.dealFrom.contracts[field]}
                  <DisplayField
                    wrapperClasses="px-4 py-2"
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
