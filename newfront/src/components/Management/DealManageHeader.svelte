<script lang="ts">
  import { _ } from "svelte-i18n";
  import type { Deal } from "$lib/types/deal";
  import ManageHeader from "./ManageHeader.svelte";

  export let deal: Deal;
  export let dealVersion: number;
</script>

<ManageHeader object={deal} objectVersion={dealVersion}>
  <div slot="heading">
    {$_("Deal")} #{deal.id}
    {#if deal.country}
      <span class="headercountry">{deal.country.name}</span>
    {/if}
  </div>
</ManageHeader>
