<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { InvestorHull } from "$lib/types/data"

  import InvolvementsGraph from "$components/New/InvolvementsGraph/InvolvementsGraph.svelte"

  export let investor: InvestorHull
</script>

{#if investor.selected_version.status === "ACTIVATED" && investor.selected_version.id === investor.active_version_id}
  <InvolvementsGraph investor_id={investor.id} />
{:else}
  <div class="m-10 bg-neutral-200 px-12 py-24 text-center text-zinc-700">
    {@html $_(
      "The investor network diagram is only available for the current active version. Go to {liveLink} to see it.",
      {
        values: {
          liveLink: `<a class="investor" href="/investor/${investor.id}/network-graph">/investor/${investor.id}/</a>`,
        },
      },
    )}
  </div>
{/if}
