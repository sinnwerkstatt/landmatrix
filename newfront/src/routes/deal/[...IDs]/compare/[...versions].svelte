<script context="module" lang="ts">
  import type { Load } from "@sveltejs/kit";
  import { diff } from "deep-object-diff";
  import type { Deal } from "$lib/types/deal";
  import { deal_gql_query } from "../../queries";

  export const load: Load = async ({ params, stuff }) => {
    let [dealID] = params.IDs.split("/").map((x) => (x ? +x : undefined));
    if (!dealID) return { status: 404, error: `Deal not found` };

    let [versionFrom, versionTo] = params.versions
      .split("/")
      .map((x) => (x ? +x : undefined));

    if (!stuff.secureApolloClient) return {};

    const vFrom = await stuff.secureApolloClient.query<Deal>({
      query: deal_gql_query,
      variables: { id: dealID, version: +versionFrom, subset: "UNFILTERED" },
      fetchPolicy: "no-cache",
    });
    const dealFrom = vFrom.data.deal;
    const vTo = await stuff.secureApolloClient.query<Deal>({
      query: deal_gql_query,
      variables: { id: dealID, version: +versionTo, subset: "UNFILTERED" },
      fetchPolicy: "no-cache",
    });
    const dealTo = vTo.data.deal;

    let dealdiffy = Object.keys(diff(dealFrom, dealTo));
    let locdiffy = Object.keys(diff(dealFrom.locations, dealTo.locations));
    let dsdiffy = Object.keys(diff(dealFrom.datasources, dealTo.datasources));
    let condiffy = Object.keys(diff(dealFrom.contracts, dealTo.contracts));

    return {
      props: {
        dealID,
        versionFrom,
        versionTo,
        dealFrom,
        dealTo,
        dealdiff: dealdiffy.length ? new Set(dealdiffy) : new Set(),
        locationsdiff: locdiffy.length ? new Set(locdiffy) : null,
        datasourcesdiff: dsdiffy.length ? new Set(dsdiffy) : null,
        contractsdiff: condiffy.length ? new Set(condiffy) : null,
      },
    };
  };
</script>

<script lang="ts">
  import { _ } from "svelte-i18n";
  import { dealSubsections } from "$lib/deal_sections";
  import { dealSections } from "$lib/deal_sections.js";
  import { formfields } from "$lib/stores";
  import DisplayField from "$components/Fields/DisplayField.svelte";

  export let versionFrom;
  export let versionTo;
  export let dealID: number;
  export let dealFrom: Deal;
  export let dealTo: Deal;
  export let dealdiff;
  export let locationsdiff;
  export let datasourcesdiff;
  export let contractsdiff;

  function anyFieldFromSection(subsections) {
    return subsections.some((subsec) => anyFieldFromSubSection(subsec));
  }
  function anyFieldFromSubSection(subsec) {
    return subsec.fields.some((f) => dealdiff.has(f));
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
    #{dealID} @{versionFrom} - @{versionTo}
  </title>
</svelte:head>

<table class="mx-4 my-12">
  <thead>
    <tr class="text-2xl">
      <th class="pl-1">
        <a href="/deal/{dealID}">{$_("Deal")} #{dealID} </a>
      </th>
      <th class="px-4">
        <a href="/deal/{dealID}/{versionFrom}">{$_("Version")} {versionFrom}</a>
      </th>
      <th> <a href="/deal/{dealID}/{versionTo}">{$_("Version")} {versionTo}</a></th>
    </tr>
  </thead>

  <tbody>
    {#each Object.entries(dealSections) as [label, section]}
      {#if anyFieldFromSection(section)}
        <tr>
          <th colspan="3" class="bg-gray-500 text-white py-4">
            <h2 class="text-xl pl-2">{labels[label]}</h2>
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
              {#if dealdiff.has(field)}
                <tr class="odd:bg-gray-100">
                  <th class="py-2 pl-8 whitespace-nowrap">
                    {$formfields.deal[field].label}
                  </th>
                  <td>
                    <DisplayField
                      wrapperClasses="px-4 py-2"
                      fieldname={field}
                      showLabel={false}
                      value={dealFrom[field]}
                    />
                  </td>
                  <td>
                    <DisplayField
                      wrapperClasses="py-2"
                      fieldname={field}
                      showLabel={false}
                      value={dealTo[field]}
                    />
                  </td>
                </tr>
              {/if}
            {/each}
          {/if}
        {/each}
      {/if}
    {/each}

    {#if locationsdiff}
      <tr class="border-t-[3rem] border-white">
        <th colspan="3" class="bg-gray-500 text-white py-4">
          <h2 class="text-xl pl-2">{$_("Locations")}</h2>
        </th>
      </tr>
      {#each [...locationsdiff] as field}
        <tr>
          <th colspan="3" class="bg-gray-300 py-2">
            <h3 class="text-lg m-0 pl-5">{$_("Location")} #{+field + 1}</h3>
          </th>
        </tr>
        {#each dealSubsections.location as jfield}
          {#if hasDifference(dealFrom.locations, dealTo.locations, field, jfield)}
            <tr class="odd:bg-gray-100">
              <th class="py-2 pl-8 whitespace-nowrap">
                {$formfields.location[jfield].label}
              </th>
              <td>
                {#if dealFrom.locations[field]}
                  <DisplayField
                    wrapperClasses="px-4 py-2"
                    fieldname={jfield}
                    showLabel={false}
                    value={dealFrom.locations[field][jfield]}
                    model="location"
                  />
                {/if}
              </td>
              <td>
                {#if dealTo.locations[field]}
                  <DisplayField
                    wrapperClasses="py-2"
                    fieldname={jfield}
                    showLabel={false}
                    value={dealTo.locations[field][jfield]}
                    model="location"
                  />
                {/if}
              </td>
            </tr>
          {/if}
        {/each}
      {/each}
    {/if}

    {#if datasourcesdiff}
      <tr class="border-t-[3rem] border-white">
        <th colspan="3" class="bg-gray-500 text-white py-4">
          <h2 class="text-xl pl-2">{$_("Data sources")}</h2>
        </th>
      </tr>
      {#each [...datasourcesdiff] as field}
        <tr>
          <th colspan="3" class="bg-gray-300 py-2">
            <h3 class="text-lg m-0 pl-5">{$_("Data source")} #{+field + 1}</h3>
          </th>
        </tr>
        {#each dealSubsections.datasource as jfield}
          {#if hasDifference(dealFrom.datasources, dealTo.datasources, field, jfield)}
            <tr class="odd:bg-gray-100">
              <th class="py-2 pl-8 whitespace-nowrap">
                {$formfields.datasource[jfield].label}
              </th>
              <td>
                {#if dealFrom.datasources[field]}
                  <DisplayField
                    wrapperClasses="px-4 py-2"
                    fieldname={jfield}
                    showLabel={false}
                    value={dealFrom.datasources[field][jfield]}
                    model="datasource"
                  />
                {/if}
              </td>
              <td>
                {#if dealTo.datasources[field]}
                  <DisplayField
                    wrapperClasses="py-2"
                    fieldname={jfield}
                    showLabel={false}
                    value={dealTo.datasources[field][jfield]}
                    model="datasource"
                  />
                {/if}
              </td>
            </tr>
          {/if}
        {/each}
      {/each}
    {/if}

    {#if contractsdiff}
      <tr class="border-t-[3rem] border-white">
        <th colspan="3" class="bg-gray-500 text-white py-4">
          <h2 class="text-xl pl-2">{$_("Contracts")}</h2>
        </th>
      </tr>
      {#each [...contractsdiff] as field}
        <tr>
          <th colspan="3" class="bg-gray-300 py-2">
            <h3 class="text-lg m-0 pl-5">{$_("Contract")} #{+field + 1}</h3>
          </th>
        </tr>
        {#each dealSubsections.contract as jfield}
          {#if hasDifference(dealFrom.contracts, dealTo.contracts, field, jfield)}
            <tr class="odd:bg-gray-100">
              <th class="py-2 pl-8 whitespace-nowrap">
                {$formfields.contract[jfield].label}
              </th>
              <td>
                {#if dealFrom.contracts[field]}
                  <DisplayField
                    wrapperClasses="px-4 py-2"
                    fieldname={jfield}
                    showLabel={false}
                    value={dealFrom.contracts[field][jfield]}
                    model="contract"
                  />
                {/if}
              </td>
              <td>
                {#if dealTo.contracts[field]}
                  <DisplayField
                    wrapperClasses="py-2"
                    fieldname={jfield}
                    showLabel={false}
                    value={dealTo.contracts[field][jfield]}
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
