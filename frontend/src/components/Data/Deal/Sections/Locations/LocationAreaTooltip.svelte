<script lang="ts">
  import type { Feature } from "ol"
  import { getArea } from "ol/sphere"
  import { _ } from "svelte-i18n"

  import { createLabels, fieldChoices } from "$lib/stores"

  import { formatArea } from "$components/Fields/Display2/jsonHelpers"

  interface Props {
    feature: Feature
  }

  let { feature }: Props = $props()

  const fprops = $derived(feature.getProperties())
  const geom = $derived(feature.getGeometry())

  const areaTypeLabels = $derived(createLabels($fieldChoices.area.type))
</script>

<div
  class="min-w-80 rounded-xl border bg-white p-4 text-sm drop-shadow-[4px_4px_5px_rgba(0,0,0,0.4)]"
>
  <div>
    <!--  <b>{$_("id")}</b>-->
    <a class="font-mono" href="#{fprops.nid}">
      #{fprops.nid}
    </a>
  </div>
  <div>
    <b>{$_("Type")}</b>
    : {areaTypeLabels[fprops.type]}
  </div>
  {#if geom}
    <div>
      <b>{$_("Size")}</b>
      {formatArea(getArea(geom))}
      {$_("ha")}
    </div>
  {/if}
  <div>
    <b>{$_("Year")}</b>
    : {fprops.date ? fprops.date : "--"}
  </div>
  <!--<div>-->
  <!--  <b>{$_("Current")}</b>-->
  <!--  : {!!feature.properties.current}-->
  <!--</div>-->
</div>
