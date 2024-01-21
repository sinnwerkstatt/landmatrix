<script lang="ts">
  import { _ } from "svelte-i18n"

  import { currencies } from "$lib/stores"

  import VirtualListSelect from "$components/LowLevel/VirtualListSelect.svelte"

  export let value: number | null
</script>

{#if $currencies}
  <VirtualListSelect
    value={$currencies.find(c => c.id === value)}
    items={$currencies}
    placeholder={$_("Currency")}
    label="name"
    on:input={e => (value = e?.detail?.id ?? null)}
  >
    <svelte:fragment slot="selection" let:selection>
      {selection.name} ({selection.code})
    </svelte:fragment>
    <svelte:fragment slot="item" let:item>
      {item.name} ({item.code})
    </svelte:fragment>
  </VirtualListSelect>
{/if}
