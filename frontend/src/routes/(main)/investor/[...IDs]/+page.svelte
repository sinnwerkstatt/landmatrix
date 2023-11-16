<script lang="ts">
  import { _ } from "svelte-i18n"

  import { invalidate } from "$app/navigation"
  import { page } from "$app/stores"

  import { loading } from "$lib/stores"
  import { UserRole } from "$lib/types/user"

  import HeaderDates from "$components/HeaderDates.svelte"

  import SectionGeneralInfo from "./SectionGeneralInfo.svelte"
  import SectionHistory from "./SectionHistory.svelte"

  export let data

  // let simpleInvolvements: Involvement[]
  // $: simpleInvolvements = [
  //   ...investor.investors.map(
  //     i =>
  //       ({
  //         ...i,
  //         role:
  //           i.role === Role.PARENT
  //             ? $_("Parent company")
  //             : $_("Tertiary investor/lender"),
  //       }) as Involvement,
  //   ),
  //   ...investor.ventures.map(
  //     i =>
  //       ({
  //         ...i,
  //         venture: undefined, // unify by renaming props: venture -> investor
  //         investor: i.venture,
  //         role:
  //           i.role === Role.PARENT
  //             ? $_("Subsidiary company")
  //             : $_("Beneficiary company"),
  //       }) as Involvement,
  //   ),
  // ]

  // $: if (!$page.data.user) {
  //   simpleInvolvements = simpleInvolvements.filter(
  //     involvement => involvement.investor.status != Status.DELETED,
  //   )
  // }

  $: activeTab = $page.url.hash.split("/")[0] || "#general"

  $: allTabs = [
    { target: "#general", name: $_("General info") },
    { target: "#involvements", name: $_("Involvements") },
    { target: "#network_graph", name: $_("Network graph") },
    { target: "#data_sources", name: $_("Data sources") },
    { target: "#history", name: $_("Version history") },
  ]

  $: tabs =
    data.investor.datasources && data.investor.datasources.length > 0
      ? allTabs
      : allTabs.filter(tab => tab.target !== "#data_sources")

  const reloadInvestor = async () => {
    loading.set(true)
    await invalidate(`/api/deal/${data.investorID}/`)
    loading.set(false)
  }

  $: liveLink = `<a href="/investor/${data.investorID}/#network_graph">https://landmatrix.org/investor/${data.investorID}/</a>`
</script>

<svelte:head>
  <title>{data.investor.selected_version.name} #{data.investor.id}</title>
</svelte:head>

<div class="container mx-auto min-h-full px-2 pb-12">
  {#if false && $page.data.user?.role > UserRole.ANYBODY}
    <!--    <InvestorManageHeader-->
    <!--      {investor}-->
    <!--      investorVersion={data.investorVersion}-->
    <!--      on:reload={reloadInvestor}-->
    <!--    />-->
  {:else}
    <div class="md:flex md:flex-row md:justify-between">
      <h1 class="heading4 mt-3">
        {data.investor.selected_version.name}
        <small>#{data.investor.id}</small>
      </h1>
      <HeaderDates obj={data.investor} />
    </div>
  {/if}

  <div class="flex min-h-full">
    <nav class="w-1/6 p-2">
      <ul>
        {#each tabs as { target, name }}
          <li
            class="whitespace-nowrap border-orange py-2 pr-20 {activeTab === target
              ? 'border-r-4'
              : 'border-r'}"
          >
            {#if name}
              <a
                href={target}
                class={activeTab === target ? "text-lm-dark dark:text-white" : ""}
              >
                {name}
              </a>
            {:else}
              <hr />
            {/if}
          </li>
        {/each}
      </ul>
    </nav>
    <div class="w-full flex-auto pl-4">
      {#if activeTab === "#general"}
        <SectionGeneralInfo version={data.investor.selected_version} />
      {/if}
      <!--{#if activeTab === "#involvements"}-->
      <!--  <h3>{$_("Involvements")} ({simpleInvolvements.length})</h3>-->
      <!--  <table class="relative mb-20 w-full table-auto">-->
      <!--    <thead class="border-b-2 dark:border-gray-800">-->
      <!--      <tr>-->
      <!--        <th>{$_("Investor ID")}</th>-->
      <!--        <th>{$_("Name")}</th>-->
      <!--        <th>{$_("Country of registration")}</th>-->
      <!--        <th>{$_("Classification")}</th>-->
      <!--        <th>{$_("Relationship")}</th>-->
      <!--        <th>{$_("Ownership share")}</th>-->
      <!--      </tr>-->
      <!--    </thead>-->
      <!--    <tbody>-->
      <!--      {#each simpleInvolvements as involvement}-->
      <!--        <tr-->
      <!--          class={involvement.investor.status === Status.DELETED-->
      <!--            ? "bg-lm-red-deleted"-->
      <!--            : ""}-->
      <!--        >-->
      <!--          <td>-->
      <!--            <DisplayField-->
      <!--              value={involvement.investor.id}-->
      <!--              valueClasses=""-->
      <!--              wrapperClasses="text-center"-->
      <!--              fieldname="id"-->
      <!--              model="investor"-->
      <!--            />-->
      <!--          </td>-->
      <!--          <td>-->
      <!--            <DisplayField-->
      <!--              value={involvement.investor.name}-->
      <!--              valueClasses=""-->
      <!--              wrapperClasses=""-->
      <!--              fieldname="name"-->
      <!--              model="investor"-->
      <!--            />-->
      <!--          </td>-->
      <!--          <td>-->
      <!--            <DisplayField-->
      <!--              value={involvement.investor.country}-->
      <!--              valueClasses=""-->
      <!--              wrapperClasses=""-->
      <!--              fieldname="country"-->
      <!--              model="investor"-->
      <!--            />-->
      <!--          </td>-->
      <!--          <td>-->
      <!--            <DisplayField-->
      <!--              value={involvement.investor.classification}-->
      <!--              valueClasses=""-->
      <!--              wrapperClasses=""-->
      <!--              fieldname="classification"-->
      <!--              model="investor"-->
      <!--            />-->
      <!--          </td>-->
      <!--          <td>{involvement.role}</td>-->
      <!--          <td>-->
      <!--            {#if involvement.percentage}-->
      <!--              {involvement.percentage} %-->
      <!--            {/if}-->
      <!--          </td>-->
      <!--        </tr>-->
      <!--      {/each}-->
      <!--    </tbody>-->
      <!--  </table>-->

      <!--  {#if investor.deals?.length > 0}-->
      <!--    <h3>-->
      <!--      {$_("Deals (Involvements as Operating company)")} ({investor.deals.length})-->
      <!--    </h3>-->

      <!--    <table class="relative w-full table-auto">-->
      <!--      <thead class="border-b-2">-->
      <!--        <tr>-->
      <!--          <th>{$_("Deal ID")}</th>-->
      <!--          <th>{$_("Target country")}</th>-->
      <!--          <th>{$_("Intention of investment")}</th>-->
      <!--          <th>{$_("Current negotiation status")}</th>-->
      <!--          <th>{$_("Current implementation status")}</th>-->
      <!--          <th>{$_("Deal size")}</th>-->
      <!--        </tr>-->
      <!--      </thead>-->
      <!--      <tbody>-->
      <!--        {#each investor.deals as deal}-->
      <!--          <tr>-->
      <!--            {#each ["id", "country", "current_intention_of_investment", "current_negotiation_status", "current_implementation_status", "deal_size"] as field}-->
      <!--              <td>-->
      <!--                <DisplayField-->
      <!--                  value={deal[field]}-->
      <!--                  valueClasses=""-->
      <!--                  wrapperClasses=""-->
      <!--                  fieldname={field}-->
      <!--                />-->
      <!--              </td>-->
      <!--            {/each}-->
      <!--          </tr>-->
      <!--        {/each}-->
      <!--      </tbody>-->
      <!--    </table>-->
      <!--  {/if}-->
      <!--{/if}-->
      <!--{#if activeTab === "#data_sources"}-->
      <!--  <DealSubmodelSection-->
      <!--    model="datasource"-->
      <!--    modelName="Data source"-->
      <!--    entries={investor.datasources}-->
      <!--  />-->
      <!--{/if}-->
      {#if activeTab === "#history"}
        <SectionHistory
          investor={data.investor}
          investorID={data.investorID}
          investorVersion={data.investorVersion}
        />
      {/if}
      <!--{#if activeTab === "#network_graph"}-->
      <!--  {#if !data.investorVersion}-->
      <!--    <InvestorGraph {investor} showControls includeVentures />-->
      <!--  {:else}-->
      <!--    <div class="m-10 bg-neutral-200 px-12 py-24 text-center text-zinc-700">-->
      <!--      {@html $_(-->
      <!--        "The investor network diagram is not visible in draft mode. Go to {liveLink} to see it.",-->
      <!--        { values: { liveLink } },-->
      <!--      )}-->
      <!--    </div>-->
      <!--  {/if}-->
      <!--{/if}-->
    </div>
  </div>
</div>
