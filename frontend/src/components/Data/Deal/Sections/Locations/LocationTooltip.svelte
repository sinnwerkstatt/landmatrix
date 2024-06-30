<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { PointFeature } from "$lib/types/data"

  export let feature: PointFeature
</script>

<div class="mb-2">
  <a class="font-mono text-lg" href="#{feature.properties.id}">
    #{feature.properties.id}
  </a>
</div>
<div>
  <b>{$_("Name")}</b>
  : {feature.properties.name}
</div>
<div>
  <b>{$_("Point")}</b>
  : {feature.geometry.coordinates}
</div>
