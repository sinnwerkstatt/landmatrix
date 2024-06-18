<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { DealHull } from "$lib/types/data"

  import CountryField from "$components/Fields/Display2/CountryField.svelte"
  import CheckCircleIcon from "$components/icons/CheckCircleIcon.svelte"
  import CheckIcon from "$components/icons/CheckIcon.svelte"
  import EyeIcon from "$components/icons/EyeIcon.svelte"
  import EyeSlashIcon from "$components/icons/EyeSlashIcon.svelte"
  import MinusCircleIcon from "$components/icons/MinusCircleIcon.svelte"
  import XIcon from "$components/icons/XIcon.svelte"
  import ManageHeader from "$components/New/ManageHeader.svelte"

  export let deal: DealHull

  $: activeVersion = deal.selected_version.id === deal.active_version_id
</script>

<ManageHeader object={deal}>
  <svelte:fragment slot="heading">
    <h1 class="heading3 my-0">Deal #{deal.id}</h1>
    <div class="heading4 my-0">
      <CountryField value={deal.country_id} />
    </div>
  </svelte:fragment>

  <svelte:fragment slot="visibility">
    <div class="mt-2 flex items-center gap-1 font-bold">
      {#if deal.selected_version.fully_updated}
        <CheckCircleIcon class="h-6 w-6 text-orange" />
        <span>{$_("Fully updated")}</span>
      {:else}
        <MinusCircleIcon class="h-6 w-6 text-gray-600" />
        <span class="text-gray-600 dark:text-white">{$_("Not fully updated")}</span>
      {/if}
    </div>
    <div class="flex items-center gap-4 bg-gray-600 px-2 py-1 text-white">
      <div class="flex items-center gap-1 text-lg">
        {#if deal.selected_version.is_public}
          <EyeIcon class="h-6 w-6 text-orange" />
          {activeVersion ? $_("Publicly visible") : $_("Will be publicly visible")}
        {:else}
          <EyeSlashIcon class="h-6 w-6 text-gray-100" />
          <span class="text-gray-100 dark:text-white">
            {activeVersion
              ? $_("Not publicly visible")
              : $_("Will not be publicly visible")}
          </span>
        {/if}
      </div>
      <ul class="">
        <li class="flex items-center gap-1 whitespace-nowrap">
          {#if deal.selected_version.datasources.length > 0}
            <CheckIcon class="mx-1 h-4 w-4" />
            {$_("At least one data source")} ({deal.selected_version.datasources
              .length})
          {:else}
            <XIcon class="mx-1 h-4 w-4" /> {$_("No data source")}
          {/if}
        </li>
        <li class="flex items-center gap-1">
          {#if deal.selected_version.has_known_investor}
            <CheckIcon class="mx-1 h-4 w-4" /> {$_("At least one active investor")}
          {:else}
            <XIcon class="mx-1 h-4 w-4" /> {$_("No known active investor")}
          {/if}
        </li>
      </ul>
    </div>
  </svelte:fragment>
</ManageHeader>
