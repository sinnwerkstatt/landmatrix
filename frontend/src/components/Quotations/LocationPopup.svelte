<script lang="ts">
  import type { Location } from "$lib/types/data"
  import type { SubmodelEntry } from "$lib/utils/dataProcessing"

  import DisplayField from "$components/Fields/DisplayField.svelte"

  interface Props {
    entry: SubmodelEntry
  }

  let { entry }: Props = $props()

  const location = $derived(entry as Location)
</script>

<DisplayField
  value={location.level_of_accuracy}
  fieldname="location.level_of_accuracy"
  showLabel
/>
<DisplayField value={location.name} fieldname="location.name" showLabel />
<DisplayField value={location.point} fieldname="location.point" showLabel />
<DisplayField value={location.description} fieldname="location.description" showLabel />
<DisplayField
  value={location.facility_name}
  fieldname="location.facility_name"
  showLabel
/>
<DisplayField value={location.comment} fieldname="location.comment" showLabel />
<!--{#if map}-->
<!--  <LocationAreasField-->
<!--    {map}-->
<!--    label={$_("Areas")}-->
<!--    areas={location.areas}-->
<!--    fieldname="location.areas"-->
<!--    isSelectedEntry={!selectedLocationId || location.nid === selectedLocationId}-->
<!--  />-->
<!--{/if}-->
