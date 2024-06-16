<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { InvestorHull } from "$lib/types/data.js"

  import ManageHeader from "$components/New/ManageHeader.svelte"

  export let investor: InvestorHull
</script>

<ManageHeader object={investor}>
  <svelte:fragment slot="heading">
    {#if investor.selected_version.name_unknown}
      <span class="italic text-gray-600">[{$_("unknown investor")}]</span>
    {:else}
      {investor.selected_version.name}
    {/if}
    <small>#{investor.id}</small>
  </svelte:fragment>
</ManageHeader>
