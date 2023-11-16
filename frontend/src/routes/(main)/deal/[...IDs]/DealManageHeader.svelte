<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { DealHull } from "$lib/types/newtypes"

  import CheckIcon from "$components/icons/CheckIcon.svelte"
  import EyeIcon from "$components/icons/EyeIcon.svelte"
  import EyeSlashIcon from "$components/icons/EyeSlashIcon.svelte"
  import XIcon from "$components/icons/XIcon.svelte"

  import DealDates from "./DealDates.svelte"

  export let deal: DealHull
  export let dealVersion: number | undefined
</script>

<div class="my-4 grid grid-cols-3">
  <div class="col-span-2 bg-gray-light ">
    <div class="flex items-center justify-between gap-4 p-2">
      <div>
        <h1 class="heading3 my-0">Deal #{deal.id}</h1>
        <div class="heading4">{deal.country.name}</div>
      </div>
      <DealDates {deal} />
      <!--      <div class="bg-white px-4 py-2">Draft version</div>-->
    </div>
    <hr class="h-0.5 bg-black" />
    <div class="p-2">
      <div class="flex items-center justify-between gap-4">
        <h2 class="heading4">Version #{deal.selected_version.id}</h2>
        <div class="flex items-center gap-4 bg-gray-dark px-2 py-1 text-white">
          <div class="flex items-center gap-1 text-lg">
            {#if deal.selected_version.is_public}
              <EyeIcon class="h-6 w-6 text-orange" /> {$_("Publicly visible")}
            {:else}
              <EyeSlashIcon class="h-6 w-6 text-lm-darkgray" />
              <span class="text-lm-darkgray dark:text-white">
                {$_("Not publicly visible")}
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
                <CheckIcon class="mx-1 h-4 w-4" /> {$_("At least one investor")}
              {:else}
                <XIcon class="mx-1 h-4 w-4" /> {$_("No known investor")}
              {/if}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
  <div class="col-span-1 h-24 bg-gray-medium p-2">huhu</div>
</div>
<!--{JSON.stringify(deal)}-->
<!--{JSON.stringify(dealVersion)}-->
