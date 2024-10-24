<script lang="ts">
  import { _ } from "svelte-i18n"

  import { filters } from "$lib/filters"
  import type { DealQIKey } from "$lib/types/data"

  import DownloadIcon from "$components/icons/DownloadIcon.svelte"

  export let qi: DealQIKey
  export let inverse: boolean

  $: dataDownloadURL = `/api/legacy_export/?${$filters.toRESTFilterArray()}&qi=${qi}&inverse=${inverse}`
</script>

<ul>
  <li>
    <a data-sveltekit-reload href={dataDownloadURL + "&format=xlsx"}>
      <DownloadIcon />
      {$_("All attributes")} (xlsx)
    </a>
  </li>
  <li>
    <a data-sveltekit-reload href={dataDownloadURL + "&format=csv"}>
      <DownloadIcon />
      {$_("All attributes")} (csv)
    </a>
  </li>
</ul>
