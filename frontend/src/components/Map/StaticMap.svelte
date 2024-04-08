<script lang="ts">
  import { _ } from "svelte-i18n"

  import { filters } from "$lib/filters"

  export let countryID: number
  export let regionID: number
  export let staticmap: string | undefined = undefined

  const onClickMap = async () => {
    if (regionID) {
      $filters.region_id = regionID
      $filters.country_id = undefined
    } else if (countryID) {
      $filters.region_id = undefined
      $filters.country_id = countryID
    }
  }
</script>

<div
  class="relative mt-6 h-[30vh] min-h-[300px] w-full cursor-pointer border border-orange shadow-md hover:border-orange-300"
>
  <a
    class="group absolute z-20 flex h-full w-full bg-transparent transition duration-300 hover:bg-orange/20"
    href="/map/"
    on:click={onClickMap}
  >
    <span
      class="z-1 hover-text invisible w-full self-center text-center text-[4rem] font-bold text-white opacity-0 transition duration-500 group-hover:visible group-hover:opacity-100"
    >
      {$_("Go to map")}
    </span>
  </a>
  {#if staticmap}
    <img src={staticmap} alt="" class="h-full w-full object-cover" />
  {/if}
</div>
