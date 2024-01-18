<script lang="ts">
  import type { Map } from "leaflet"
  import { _ } from "svelte-i18n"
  import { slide } from "svelte/transition"

  import { newNanoid } from "$lib/helpers"
  import { fieldChoices } from "$lib/stores"
  import { Location2 } from "$lib/types/newtypes"
  import type { Country } from "$lib/types/wagtail"
  import { isEmptySubmodel } from "$lib/utils/data_processing"
  import { createLegend } from "$lib/utils/location"

  import ChoicesField from "$components/Fields/Edit2/ChoicesField.svelte"
  import PointField from "$components/Fields/Edit2/PointField.svelte"
  import TextField from "$components/Fields/Edit2/TextField.svelte"
  import PlusIcon from "$components/icons/PlusIcon.svelte"
  import TrashIcon from "$components/icons/TrashIcon.svelte"
  import BigMap from "$components/Map/BigMap.svelte"

  import LocationAreasField from "./LocationAreasField.svelte"
  import LocationGoogleField from "./LocationGoogleField.svelte"

  export let locations: Location2[]
  export let country: Country
  let activeEntryIdx = -1

  let map: Map | undefined

  function addEntry() {
    const currentIDs = locations.map(entry => entry.nid)
    locations = [...locations, new Location2(newNanoid(currentIDs))]
    activeEntryIdx = locations.length - 1
  }

  function toggleActiveEntry(index: number): void {
    activeEntryIdx = activeEntryIdx === index ? -1 : index
  }

  function removeEntry(c: Location2) {
    if (!isEmptySubmodel(c)) {
      const areYouSure = confirm(`${$_("Remove")} ${$_("Location")} #${c.nid}?`)
      if (!areYouSure) return
    }
    locations = locations.filter(x => x.nid !== c.nid)
  }

  const onMapReady = (e: CustomEvent<Map>) => {
    map = e.detail
    // map.addControl(createLegend())
  }
  const onGoogleLocationAutocomplete = (
    event: CustomEvent<{ latLng: [number, number]; viewport: unknown }>,
  ) => {}
</script>

<section class="lg:h-full">
  <form class="flex flex-wrap lg:h-full" id="locations">
    <div class="w-full overflow-y-auto p-2 lg:h-full lg:w-2/5">
      {#each locations as location, index}
        <div class="location-entry">
          <div
            class="my-2 flex flex-row items-center justify-between bg-gray-200 dark:bg-gray-700"
          >
            <div
              role="button"
              class="flex-grow p-2"
              on:click={() => toggleActiveEntry(index)}
              on:keydown={e => e.code === "Enter" && toggleActiveEntry(index)}
              tabindex="0"
            >
              <h3 class="m-0">
                {index + 1}. {$_("Location")}
                <small class="text-sm text-gray-500">
                  #{location.nid}
                </small>
              </h3>
            </div>
            <button
              class="flex-initial p-2"
              on:click|stopPropagation={() => removeEntry(location)}
            >
              <TrashIcon class="h-8 w-6 cursor-pointer text-red-600" />
            </button>
          </div>
          {#if activeEntryIdx === index}
            <!--{JSON.stringify(location)}-->
            <div transition:slide={{ duration: 200 }}>
              <ChoicesField
                fieldname="location.level_of_accuracy"
                bind:value={location.level_of_accuracy}
                label={$_("Spatial accuracy level")}
                choices={$fieldChoices.deal.level_of_accuracy}
                required
              />
              <LocationGoogleField
                fieldname="location.name"
                bind:value={location.name}
                countryCode={country.code_alpha2}
                on:change={onGoogleLocationAutocomplete}
                label={$_("Location")}
              />
              <PointField
                fieldname="location.point"
                bind:value={location.point}
                label={$_("Point")}
              />
              <TextField
                fieldname="location.description"
                bind:value={location.description}
                label={$_("Description")}
                multiline
              />
              <TextField
                fieldname="location.facility_name"
                bind:value={location.facility_name}
                label={$_("Facility name")}
              />
              <TextField
                fieldname="location.comment"
                bind:value={location.comment}
                label={$_("Comment")}
                multiline
              />
              <!--            <LocationAreasField bind:areas={locations[activeEntryIdx].areas} />-->
            </div>
          {/if}
        </div>
      {/each}
      <div class="mt-6">
        <button
          class="btn btn-primary flex items-center"
          on:click={addEntry}
          type="button"
        >
          <PlusIcon class="-ml-2 mr-2 h-6 w-5" />
          {$_("Add")}
          {$_("Location")}
        </button>
      </div>
    </div>
    <div class="w-full p-2 lg:h-full lg:w-3/5">
      <BigMap
        containerClass="h-[400px] lg:h-2/3"
        on:ready={onMapReady}
        options={{ center: [0, 0] }}
      />
      <div class="overflow-y-auto p-2 lg:h-1/3">
        {#if activeEntryIdx !== -1}
          <LocationAreasField bind:areas={locations[activeEntryIdx].areas} />
        {/if}
      </div>
    </div>
  </form>
</section>
