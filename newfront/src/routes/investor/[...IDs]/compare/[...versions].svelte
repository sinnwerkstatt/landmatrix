<script context="module" lang="ts">
  import type { Load } from "@sveltejs/kit";
  import { diff } from "deep-object-diff";
  import { investor_gql_query } from "$lib/investor_queries";
  import type { Investor } from "$lib/types/investor";

  export const load: Load = async ({ params, stuff }) => {
    let [investorID] = params.IDs.split("/").map((x) => (x ? +x : undefined));
    if (!investorID) return { status: 404, error: `Investor not found` };

    let [versionFrom, versionTo] = params.versions
      .split("/")
      .map((x) => (x ? +x : undefined));

    const vFrom = await stuff.urqlClient
      .query(
        investor_gql_query,
        {
          id: investorID,
          version: +versionFrom,
          subset: "UNFILTERED",
          includeDeals: false,
        },
        { requestPolicy: "network-only" }
      )
      .toPromise();
    const investorFrom = vFrom.data.investor;
    const vTo = await stuff.urqlClient
      .query(
        investor_gql_query,
        {
          id: investorID,
          version: +versionTo,
          subset: "UNFILTERED",
          includeDeals: false,
        },
        { requestPolicy: "network-only" }
      )
      .toPromise();
    const investorTo = vTo.data.investor;

    let investordiffy = Object.keys(diff(investorFrom, investorTo));
    // let locdiffy = Object.keys(diff(investorFrom.locations, investorTo.locations));
    let dsdiffy = Object.keys(diff(investorFrom.datasources, investorTo.datasources));
    // let condiffy = Object.keys(diff(investorFrom.contracts, investorTo.contracts));

    return {
      props: {
        investorID,
        versionFrom,
        versionTo,
        investorFrom,
        investorTo,
        investordiff: investordiffy.length ? new Set(investordiffy) : new Set(),
        datasourcesdiff: dsdiffy.length ? new Set(dsdiffy) : null,
      },
    };
  };
</script>

<script lang="ts">
  import { _ } from "svelte-i18n";
  import { investorSections, subsections } from "$lib/sections";
  import { formfields } from "$lib/stores";
  import DisplayField from "$components/Fields/DisplayField.svelte";

  export let versionFrom;
  export let versionTo;
  export let investorID: number;
  export let investorFrom: Investor;
  export let investorTo: Investor;
  export let investordiff;
  export let datasourcesdiff;

  function anyFieldFromSection(subsections) {
    return subsections.some((subsec) => anyFieldFromSubSection(subsec));
  }
  function anyFieldFromSubSection(subsec) {
    return subsec.fields.some((f) => investordiff.has(f));
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
    #{investorID} @{versionFrom} - @{versionTo}
  </title>
</svelte:head>

<table class="mx-4 my-12">
  <thead>
    <tr class="text-2xl">
      <th class="pl-1">
        <a href="/investor/{investorID}">{$_("Investor")} #{investorID} </a>
      </th>
      <th class="px-4">
        <a href="/investor/{investorID}/{versionFrom}">{$_("Version")} {versionFrom}</a>
      </th>
      <th>
        <a href="/investor/{investorID}/{versionTo}">{$_("Version")} {versionTo}</a></th
      >
    </tr>
  </thead>

  <tbody>
    {#each Object.entries(investorSections) as [label, section]}
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
              {#if investordiff.has(field)}
                <tr class="odd:bg-gray-100">
                  <th class="py-2 pl-8 whitespace-nowrap">
                    {$formfields.investor[field].label}
                  </th>
                  <td>
                    <DisplayField
                      wrapperClasses="px-4 py-2"
                      fieldname={field}
                      value={investorFrom[field]}
                      model="investor"
                    />
                  </td>
                  <td>
                    <DisplayField
                      wrapperClasses="py-2"
                      fieldname={field}
                      value={investorTo[field]}
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
        {#each subsections.datasource as jfield}
          {#if hasDifference(investorFrom.datasources, investorTo.datasources, field, jfield)}
            <tr class="odd:bg-gray-100">
              <th class="py-2 pl-8 whitespace-nowrap">
                {$formfields.datasource[jfield].label}
              </th>
              <td>
                {#if investorFrom.datasources?.[field]}
                  <DisplayField
                    wrapperClasses="px-4 py-2"
                    fieldname={jfield}
                    value={investorFrom.datasources[field][jfield]}
                    model="datasource"
                  />
                {/if}
              </td>
              <td>
                {#if investorTo.datasources?.[field]}
                  <DisplayField
                    wrapperClasses="py-2"
                    fieldname={jfield}
                    value={investorTo.datasources[field][jfield]}
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
