<script lang="ts">
  import { queryStore } from "@urql/svelte"
  import { _ } from "svelte-i18n"
  import type { ComponentType } from "svelte"
  import { onMount } from "svelte"

  import { page } from "$app/stores"

  import { dealsQuery } from "$lib/dealQueries"
  import { filters, publicOnly } from "$lib/filters"
  import { loading, isMobile } from "$lib/stores"

  import ChartsContainer from "$components/Data/Charts/ChartsContainer.svelte"
  import DynamicsOfDeal from "$components/Data/Charts/CountryProfile/DynamicsOfDeal.svelte"
  import IntentionsPerCategory from "$components/Data/Charts/CountryProfile/IntentionsPerCategory.svelte"
  import LSLAByNegotiation from "$components/Data/Charts/CountryProfile/LSLAByNegotiation.svelte"
  import LoadingPulse from "$components/LoadingPulse.svelte"
  import CumulativeNumberOfDeals from "$components/Data/Charts/CountryProfile/CumulativeNumberOfDeals.svelte"
  import CumulativeSizeUnderContract from "$components/Data/Charts/CountryProfile/CumulativeSizeUnderContract.svelte"
  import LACP from "$components/Data/Charts/CountryProfile/LACP.svelte"
  import { showContextBar, showFilterBar } from "$components/Data/stores"

  interface CountryProfile {
    component: ComponentType
    label: string
    key: string
  }

  let countryProfiles: CountryProfile[]
  $: countryProfiles = [
    {
      key: "lacp",
      label: $_("Land acquisitions by category of production"),
      component: LACP,
    },
    {
      key: "lsla",
      label: $_("LSLA by negotiation status"),
      component: LSLAByNegotiation,
    },
    {
      key: "dynamicsOfDeal",
      label: $_("Dynamics of deal by investor type"),
      component: DynamicsOfDeal,
    },
    {
      key: "intentions",
      label: $_("Number of intentions per category of production"),
      component: IntentionsPerCategory,
    },
    {
      key: "cumCount",
      label: $_("Concluded deals over time since the year {year}", {
        values: { year: 2000 },
      }),
      component: CumulativeNumberOfDeals,
    },
    {
      key: "cumSize",
      label: $_("Cumulative area size under contract since the year {year}", {
        values: { year: 2000 },
      }),
      component: CumulativeSizeUnderContract,
    },
  ]

  let currentProfileKey = "lacp"
  $: currentProfile = countryProfiles.find(profile => profile.key === currentProfileKey)

  $: deals = queryStore({
    client: $page.data.urqlClient,
    query: dealsQuery,
    variables: {
      filters: $filters.toGQLFilterArray(),
      subset: $publicOnly ? "PUBLIC" : "ACTIVE",
    },
  })
  $: loading.set($deals?.fetching ?? false)

  onMount(() => {
    showContextBar.set(!$isMobile)
    showFilterBar.set(!$isMobile)
  })
</script>

<svelte:head>
  <title>{$_("Country profile graphs")} | {$_("Land Matrix")}</title>
</svelte:head>

<ChartsContainer>
  <div class="h-full w-full overflow-visible">
    {#if $deals.fetching}
      <LoadingPulse />
    {:else if $deals.error}
      <p>Error...{$deals.error.message}</p>
    {:else}
      <svelte:component this={currentProfile?.component} deals={$deals.data.deals} />
    {/if}
  </div>

  <div slot="ContextBar">
    <h2>{$_("Country profile graphs")}</h2>
    <ul>
      {#each countryProfiles as profile (profile.key)}
        <li>
          <button
            class="btn btn-secondary w-full whitespace-normal text-left font-bold"
            on:click={() => {
              currentProfileKey = profile.key
            }}
          >
            {profile.label}
          </button>
        </li>
      {/each}
    </ul>
  </div>
</ChartsContainer>
