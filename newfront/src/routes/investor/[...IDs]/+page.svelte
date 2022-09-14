<script lang="ts">
  import type { Client } from "@urql/svelte"
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import { investor_gql_query } from "$lib/investor_queries"
  import { loading } from "$lib/stores"
  import { Role } from "$lib/types/investor"
  import type { Investor } from "$lib/types/investor"
  import { UserRole } from "$lib/types/user"

  import DealSubmodelSection from "$components/Deal/DealSubmodelSection.svelte"
  import DateTimeField from "$components/Fields/Display/DateTimeField.svelte"
  import DisplayField from "$components/Fields/DisplayField.svelte"
  import InvestorGraph from "$components/Investor/InvestorGraph.svelte"
  import InvestorHistory from "$components/Investor/InvestorHistory.svelte"
  import InvestorManageHeader from "$components/Management/InvestorManageHeader.svelte"

  // import type { PageData } from "./$types";
  //
  // export let data: PageData;
  export let data: {
    investor: Investor
    investorID: number
    investorVersion: number | undefined
  }

  let investor: Investor = data.investor
  $: investor = data.investor

  $: simple_involvements = [
    ...investor.investors.map(i => ({
      ...i,
      role:
        i.role === Role.PARENT ? $_("Parent company") : $_("Tertiary investor/lender"),
    })),
    ...investor.ventures.map(i => ({
      ...i,
      investor: i.venture,
      role:
        i.role === Role.PARENT ? $_("Subsidiary company") : $_("Beneficiary company"),
    })),
  ]

  $: activeTab = $page.url.hash.split("/")[0] || "#general"

  $: tabs = [
    { target: "#general", name: $_("General info") },
    { target: "#involvements", name: $_("Involvements") },
    { target: "#network_graph", name: $_("Network graph") },
    { target: "#data_sources", name: $_("Data sources") },
    { target: "#history", name: $_("Version history") },
  ]

  async function reloadInvestor() {
    console.log("Investor detail: reload")
    loading.set(true)
    const ret = (
      await ($page.data.urqlClient as Client)
        .query<{ investor: Investor }>(
          investor_gql_query,
          {
            id: data.investorID,
            version: data.investorVersion,
            includeDeals: true,
            depth: 5, // max depth
          },
          { requestPolicy: "network-only" },
        )
        .toPromise()
    ).data
    investor = ret.investor
    loading.set(false)
  }

  onMount(reloadInvestor)
  $: liveLink = `<a href="/investor/${data.investorID}/#network_graph">https://landmatrix.org/investor/${data.investorID}/</a>`
</script>

<svelte:head>
  <title>{investor.name} #{investor.id}</title>
</svelte:head>

<div class="container mx-auto min-h-full px-2 pb-12">
  {#if $page.data.user?.role > UserRole.ANYBODY}
    <InvestorManageHeader
      {investor}
      investorVersion={data.investorVersion}
      on:reload={reloadInvestor}
    />
  {:else}
    <div class="md:flex md:flex-row md:justify-between">
      <h1>
        {investor.name}
        <small>#{investor.id}</small>
      </h1>
      <div class="my-2 flex w-auto items-center rounded bg-gray-50 p-3">
        <div class="mr-10 text-xs text-lm-dark md:mx-5 md:text-sm">
          {$_("Created")}
          <br />
          <DateTimeField value={investor.created_at} />
        </div>
        <div class="mr-10 text-xs text-lm-dark md:mx-5 md:text-sm">
          {$_("Last update")}
          <br />
          <DateTimeField value={investor.modified_at} />
        </div>
      </div>
    </div>
  {/if}

  <div class="flex min-h-full">
    <nav class="flex-initial p-2">
      <ul>
        {#each tabs as { target, name }}
          <li
            class="whitespace-nowrap border-orange py-2 pr-20 {activeTab === target
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
    <div class="w-full flex-auto pl-4">
      {#if activeTab === "#general"}
        {#each ["name", "country", "classification", "homepage", "opencorporates", "comment"] as fieldname}
          <DisplayField
            {fieldname}
            value={investor[fieldname]}
            model="investor"
            showLabel
          />
        {/each}
      {/if}
      {#if activeTab === "#involvements"}
        <h3>{$_("Involvements")} ({simple_involvements.length})</h3>
        <table class="relative mb-20 w-full table-auto">
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
                    value={involvement.investor.id}
                    valueClasses=""
                    wrapperClasses="text-center"
                    fieldname="id"
                    model="investor"
                  />
                </td>
                <td>
                  <DisplayField
                    value={involvement.investor.name}
                    valueClasses=""
                    wrapperClasses=""
                    fieldname="name"
                    model="investor"
                  />
                </td>
                <td>
                  <DisplayField
                    value={involvement.investor.country}
                    valueClasses=""
                    wrapperClasses=""
                    fieldname="country"
                    model="investor"
                  />
                </td>
                <td>
                  <DisplayField
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

          <table class="relative w-full  table-auto">
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
        <InvestorHistory
          {investor}
          investorID={data.investorID}
          investorVersion={data.investorVersion}
        />
      {/if}
      {#if activeTab === "#network_graph"}
        {#if !data.investorVersion}
          <InvestorGraph {investor} showControls />
        {:else}
          <div class="m-10 bg-neutral-200 px-12 py-24 text-center text-zinc-700">
            {@html $_(
              "The investor network diagram is not visible in draft mode. Go to {liveLink} to see it.",
              { values: { liveLink } },
            )}
          </div>
        {/if}
      {/if}
    </div>
  </div>
</div>
