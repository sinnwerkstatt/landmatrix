<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { components } from "$lib/openAPI"

  import { a_download } from "$components/Data/Charts/utils"
  import DownloadIcon from "$components/icons/DownloadIcon.svelte"

  export let counts: components["schemas"]["QICountsResponse"] | null

  const download = async () => {
    a_download(
      "data:application/json;charset=utf-8," +
        encodeURIComponent(JSON.stringify(counts)),
      "data-quality-indicators.json",
    )
  }
</script>

<div class="space-x-2">
  <span class="italic after:content-[':']">
    {$_("Download quality indicators")}
  </span>
  <button type="button" on:click={download} title={$_("Download statistics")}>
    <DownloadIcon class="h-5 w-5" />
  </button>
</div>
