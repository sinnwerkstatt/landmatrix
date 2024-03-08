<script lang="ts">
  import { _ } from "svelte-i18n"

  import { invalidate } from "$app/navigation"
  import { page } from "$app/stores"

  import { loading } from "$lib/stores"
  import { UserRole } from "$lib/types/user"

  import CountryField from "$components/Fields/Display2/CountryField.svelte"
  import HeaderDatesWDownload from "$components/HeaderDatesWDownload.svelte"
  import ManageHeaderOldVersionNote from "$components/New/ManageHeaderOldVersionNote.svelte"

  import DealManageHeader from "./DealManageHeader.svelte"

  export let data

  let tabs: { target: string; name: string | null }[]
  $: tabs = [
    { target: "locations/", name: $_("Locations") },
    { target: "general/", name: $_("General info") },
    { target: "contracts/", name: $_("Contracts") },
    { target: "employment/", name: $_("Employment") },
    { target: "investor_info/", name: $_("Investor info") },
    { target: "data_sources/", name: $_("Data sources") },
    {
      target: "local_communities/",
      name: $_("Local communities / indigenous peoples"),
    },
    { target: "former_use/", name: $_("Former use") },
    { target: "produce_info/", name: $_("Produce info") },
    { target: "water/", name: $_("Water") },
    { target: "gender_related_info/", name: $_("Gender-related info") },
    { target: "overall_comment/", name: $_("Overall comment") },
    { target: "blank1/", name: null },
    { target: "history/", name: $_("Deal history") },
  ]

  const reloadDeal = async () => {
    loading.set(true)
    await invalidate("deal:detail")
    loading.set(false)
  }

  $: selfLink = data.dealVersion
    ? `/deal/${data.dealID}/${data.dealVersion}/`
    : `/deal/${data.dealID}/`
</script>

<svelte:head>
  <title>
    {$_("Deal")} #{data.deal.id}
  </title>
</svelte:head>

<div class="container mx-auto mb-12 mt-8 min-h-full">
  <ManageHeaderOldVersionNote obj={data.deal} />
  {#if $page.data.user?.role > UserRole.ANYBODY}
    <DealManageHeader deal={data.deal} on:reload={reloadDeal} />
  {:else}
    <div class="my-4 md:flex md:flex-row md:justify-between">
      <div class="flex flex-col">
        <h1 class="heading3 mb-0 mt-3">
          {$_("Deal")}
          #{data.deal.id}
          {#if data.deal.selected_version.id !== data.deal.active_version_id}
            <span class="text-[0.9em]">
              {$_("Version")} #{data.deal.selected_version.id}
            </span>
          {/if}
        </h1>
        <div class="heading4 my-0">
          <CountryField value={data.deal.country_id} />
        </div>
      </div>
      <HeaderDatesWDownload obj={data.deal} />
    </div>
  {/if}

  <div class="flex min-h-full">
    <nav class="w-1/6 p-2">
      <ul>
        {#each tabs as { target, name }}
          {@const activeTab = `${selfLink}${target}` === $page.url.pathname}
          <li class="border-orange py-2 pr-4 {activeTab ? 'border-r-4' : 'border-r'}">
            {#if name}
              <a
                href="{selfLink}{target}"
                class={activeTab ? "text-gray-700 dark:text-white" : ""}
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
    <div class="w-5/6 px-4">
      <slot />
    </div>
  </div>
</div>
