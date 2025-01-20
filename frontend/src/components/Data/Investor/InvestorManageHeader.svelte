<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { InvestorHull } from "$lib/types/data"

  import ManageHeader from "$components/New/ManageHeader.svelte"

  interface Props {
    investor: InvestorHull
  }

  let { investor }: Props = $props()
</script>

<ManageHeader object={investor}>
  {#snippet heading()}
    {#if investor.selected_version.name_unknown}
      <span class="italic text-gray-600 dark:text-gray-400">
        [{$_("unknown investor")}]
      </span>
    {:else}
      {investor.selected_version.name}
    {/if}
    <small>#{investor.id}</small>
  {/snippet}
</ManageHeader>
