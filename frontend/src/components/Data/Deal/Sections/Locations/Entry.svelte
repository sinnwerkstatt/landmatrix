<script lang="ts">
  import type { Point } from "geojson"
  import type { Map } from "ol"

  import type { components } from "$lib/openAPI"
  import type { Location2 } from "$lib/types/data"

  import LocationAreasEditField from "$components/Data/Deal/Sections/Locations/LocationAreasEditField.svelte"
  import EditField from "$components/Fields/EditField.svelte"

  interface Props {
    entry: Location2
    extras: {
      country?: components["schemas"]["Country"]
      map?: Map
    }
    onchange?: () => void
  }

  let { entry = $bindable(), extras, onchange }: Props = $props()

  const onGoogleAutocomplete = (point: Point) => {
    entry.point = point
    onchange?.()
  }
</script>

<EditField
  fieldname="location.level_of_accuracy"
  bind:value={entry.level_of_accuracy}
  extras={{ required: true }}
  showLabel
  {onchange}
/>
<EditField
  fieldname="location.name"
  bind:value={entry.name}
  extras={{
    countryCode: extras.country?.code_alpha2,
    onGoogleAutocomplete,
  }}
  showLabel
  {onchange}
/>
<EditField fieldname="location.point" bind:value={entry.point} showLabel {onchange} />
<EditField
  fieldname="location.description"
  bind:value={entry.description}
  showLabel
  {onchange}
/>
<EditField
  fieldname="location.facility_name"
  bind:value={entry.facility_name}
  showLabel
  {onchange}
/>
<EditField
  fieldname="location.comment"
  bind:value={entry.comment}
  showLabel
  {onchange}
/>
{#if extras.map}
  <LocationAreasEditField
    bind:areas={entry.areas}
    map={extras.map}
    isSelectedEntry
    {onchange}
  />
{/if}
