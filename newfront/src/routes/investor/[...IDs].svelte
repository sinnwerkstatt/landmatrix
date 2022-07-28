<script context="module" lang="ts">
  import type { Load } from "@sveltejs/kit";
  import type { Investor } from "$lib/types/investor";
  import { investor_gql_query } from "./queries";

  export const load: Load = async ({ params, stuff }) => {
    let [investorID, investorVersion] = params.IDs.split("/").map((x) =>
      x ? +x : undefined
    );

    if (!investorID) return { status: 404, error: `Deal not found` };

    const { data } = await stuff.secureApolloClient.query<{ investor: Investor }>({
      query: investor_gql_query,
      variables: {
        id: investorID,
        version: investorVersion,
        subset: "UNFILTERED",
        includeDeals: true,
        depth: 0,
      },
    });

    return { props: { investorID, investorVersion, investor: data.investor } };
  };
</script>

<script lang="ts">
  import { _ } from "svelte-i18n";
  import { page } from "$app/stores";
  import { loading } from "$lib/data";
  import { Role } from "$lib/types/investor";
  import { UserLevel } from "$lib/types/user.js";
  import DealSubmodelSection from "$components/Deal/DealSubmodelSection.svelte";
  import DateTimeField from "$components/Fields/Display/DateTimeField.svelte";
  import DisplayField from "$components/Fields/DisplayField.svelte";
  import DownloadIcon from "$components/icons/DownloadIcon.svelte";
  import InvestorGraph from "$components/Investor/InvestorGraph.svelte";
  import InvestorManageHeader from "$components/Management/InvestorManageHeader.svelte";

  export let investor: Investor;
  export let investorID: number;
  export let investorVersion: number;

  $: simple_involvements = [
    ...investor.investors.map((i) => ({
      ...i,
      role:
        i.role === Role.PARENT ? $_("Parent company") : $_("Tertiary investor/lender"),
    })),
    ...investor.ventures.map((i) => ({
      ...i,
      investor: i.venture,
      role:
        i.role === Role.PARENT ? $_("Subsidiary company") : $_("Beneficiary company"),
    })),
  ];

  $: activeTab = $page.url.hash || "#general";

  $: tabs = [
    { target: "#general", name: $_("General info") },
    { target: "#involvements", name: $_("Involvements") },
    { target: "#data_sources", name: $_("Data sources") },
    { target: "#history", name: $_("Version History") },
  ];

  async function reloadInvestor() {
    loading.set(true);
    const { data } = await $page.stuff.secureApolloClient.query<{ investor: Investor }>(
      {
        query: investor_gql_query,
        variables: {
          id: investorID,
          version: investorVersion,
          subset: "UNFILTERED",
          includeDeals: true,
          depth: 0,
        },
        fetchPolicy: "no-cache",
      }
    );
    investor = data.investor;
    loading.set(false);
  }

  let graphDataIsReady = false;

  const download_link = function (format: string): string {
    return `/api/legacy_export/?investor_id=${investorID}&subset=UNFILTERED&format=${format}`;
  };
</script>

<svelte:head>
  <title>{investor.name} #{investor.id}</title>
</svelte:head>

<div class="container mx-auto min-h-full px-2 pb-12">
  {#if $page.stuff.user?.level > UserLevel.ANYBODY}
    <InvestorManageHeader {investor} {investorVersion} on:reload={reloadInvestor} />
  {:else}
    <div class="md:flex md:flex-row md:justify-between">
      <h1>{investor.name} <small>#{investor.id}</small></h1>
      <div class="flex items-center bg-gray-50 rounded p-3 my-2 w-auto">
        <div class="mr-10 md:mx-5 text-xs md:text-sm text-lm-dark">
          {$_("Created")}<br />
          <DateTimeField value={investor.created_at} />
        </div>
        <div class="mr-10 md:mx-5 text-xs md:text-sm text-lm-dark">
          {$_("Last update")}<br />
          <DateTimeField value={investor.modified_at} />
        </div>
      </div>
    </div>
  {/if}
  <div class="flex min-h-full">
    <nav class="p-2 flex-initial">
      <ul>
        {#each tabs as { target, name }}
          <li
            class="py-2 pr-20 border-orange whitespace-nowrap {activeTab === target
              ? 'border-r-4'
              : 'border-r'}"
          >
            {#if name}
              <a href={target} class:text-black={activeTab === target}>{name}</a>
            {:else}
              <hr />
            {/if}
          </li>
        {/each}
      </ul>
    </nav>
    <div class="pl-4 flex-auto w-full">
      {#if activeTab === "#general"}
        {#each ["name", "country", "classification", "homepage", "opencorporates", "comment"] as fieldname}
          <DisplayField {fieldname} value={investor[fieldname]} model="investor" />
        {/each}
      {/if}
      {#if activeTab === "#involvements"}
        <h3>{$_("Involvements")} ({simple_involvements.length})</h3>
        <table class="table-auto w-full relative mb-20">
          <thead class="border-b-2 ">
            <tr>
              <th>{$_("Investor ID")}</th>
              <th>{$_("Name")}</th>
              <th>{$_("Country of registration")}</th>
              <th>{$_("Classification")}</th>
              <th>{$_("Relationship")}</th>
              <th>{$_("Ownership share")}</th>
            </tr>
          </thead>
          <tbody>
            {#each simple_involvements as involvement}
              <tr>
                <td>
                  <DisplayField
                    showLabel={false}
                    value={involvement.investor.id}
                    valueClasses=""
                    wrapperClasses="text-center"
                    fieldname="id"
                    model="investor"
                  />
                </td>
                <td>
                  <DisplayField
                    showLabel={false}
                    value={involvement.investor.name}
                    valueClasses=""
                    wrapperClasses=""
                    fieldname="name"
                    model="investor"
                  />
                </td>
                <td>
                  <DisplayField
                    showLabel={false}
                    value={involvement.investor.country}
                    valueClasses=""
                    wrapperClasses=""
                    fieldname="country"
                    model="investor"
                  />
                </td>
                <td>
                  <DisplayField
                    showLabel={false}
                    value={involvement.investor.classification}
                    valueClasses=""
                    wrapperClasses=""
                    fieldname="classification"
                    model="investor"
                  />
                </td>
                <td>{involvement.role}</td>
                <td>
                  {#if involvement.percentage}
                    {involvement.percentage} %
                  {/if}
                </td>
              </tr>
            {/each}
          </tbody>
        </table>

        {#if investor.deals?.length > 0}
          <h3>
            {$_("Deals (Involvements as Operating company)")} ({investor.deals.length})
          </h3>

          <table class="table-auto w-full  relative">
            <thead class="border-b-2">
              <tr>
                <th>{$_("Deal ID")}</th>
                <th>{$_("Target country")}</th>
                <th>{$_("Intention of investment")}</th>
                <th>{$_("Current negotiation status")}</th>
                <th>{$_("Current implementation status")}</th>
                <th>{$_("Deal size")}</th>
              </tr>
            </thead>
            <tbody>
              {#each investor.deals as deal}
                <tr>
                  {#each ["id", "country", "current_intention_of_investment", "current_negotiation_status", "current_implementation_status", "deal_size"] as field}
                    <td>
                      <DisplayField
                        showLabel={false}
                        value={deal[field]}
                        valueClasses=""
                        wrapperClasses=""
                        fieldname={field}
                      />
                    </td>
                  {/each}
                </tr>
              {/each}
            </tbody>
          </table>
        {/if}
      {/if}
      {#if activeTab === "#data_sources"}
        <DealSubmodelSection
          model="datasource"
          modelName="Data source"
          entries={investor.datasources}
        />
      {/if}
      {#if activeTab === "#history"}
        <section>
          <h3>{$_("Version history")}</h3>
        </section>
      {/if}
    </div>
  </div>
  <div class="flex">
    {#if !investorVersion}
      <div class:loading_wrapper={!graphDataIsReady} class="lg:w-3/4 xl:w-1/2 mb-3">
        {#if graphDataIsReady}
          <InvestorGraph initDepth="depth" {investor} AtnewDepth="onNewDepth" />
        {/if}
      </div>
    {:else}
      <div
        class="lg:w-3/4 xl:w-1/2 mb-3 flex text-center items-center text-zinc-600 bg-neutral-300"
      >
        {$_(
          "The investor network diagram is only visible for live versions of an investor. I.e. https://landmatrix.org/investor/:id/"
        )}
      </div>
    {/if}
  </div>
</div>
