<script lang="ts" xmlns:svelte="http://www.w3.org/1999/html">
  import { _ } from "svelte-i18n"

  import type { InvestorHull } from "$lib/types/newtypes.js"

  import ManageHeader from "$components/New/ManageHeader.svelte"

  export let investor: InvestorHull
  export let investorVersion: number | undefined
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
