<script lang="ts">
  import { area as turfArea } from "@turf/turf"
  import { _ } from "svelte-i18n"

  import { createLabels, fieldChoices } from "$lib/stores"
  import type { AreaFeature, AreaType } from "$lib/types/data"

  import { formatArea } from "$components/Fields/Display2/jsonHelpers"

  export let feature: AreaFeature

  $: areaTypeLabels = createLabels<AreaType>($fieldChoices.area.type)
</script>

<div>
  <!--  <b>{$_("id")}</b>-->
  <a class="font-mono" href="#{feature.properties.id}">
    #{feature.properties.id}
  </a>
</div>
<div>
  <b>{$_("Type")}</b>
  : {areaTypeLabels[feature.properties.type]}
</div>
<div>
  <b>{$_("Size")}</b>
  : {formatArea(turfArea(feature))}
  {$_("ha")}
</div>
<div>
  <b>{$_("Year")}</b>
  : {feature.properties.date ? feature.properties.date : "--"}
</div>
<!--<div>-->
<!--  <b>{$_("Current")}</b>-->
<!--  : {!!feature.properties.current}-->
<!--</div>-->
