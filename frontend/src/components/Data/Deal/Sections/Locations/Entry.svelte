<script lang="ts">
  import type { Point } from "geojson"
  import { Map } from "leaflet?client"

  import type { components } from "$lib/openAPI"
  import type { Location2 } from "$lib/types/newtypes"

  import LocationAreasEditField from "$components/Data/Deal/Sections/Locations/LocationAreasEditField.svelte"
  import EditField from "$components/Fields/EditField.svelte"

  export let entry: Location2
  export let extras: {
    country?: components["schemas"]["Country"]
    map?: Map
  }

  const onGoogleAutocomplete = (point: Point) => {
    entry.point = point
  }
</script>

<EditField
  fieldname="location.level_of_accuracy"
  bind:value={entry.level_of_accuracy}
  extras={{ required: true }}
  showLabel
/>
<EditField
  fieldname="location.name"
  bind:value={entry.name}
  extras={{
    countryCode: extras.country?.code_alpha2,
    onGoogleAutocomplete,
  }}
  showLabel
/>
<EditField fieldname="location.point" bind:value={entry.point} showLabel />
<EditField fieldname="location.description" bind:value={entry.description} showLabel />
<EditField
  fieldname="location.facility_name"
  bind:value={entry.facility_name}
  showLabel
/>
<EditField fieldname="location.comment" bind:value={entry.comment} showLabel />
<LocationAreasEditField bind:areas={entry.areas} map={extras.map} isSelectedEntry />
