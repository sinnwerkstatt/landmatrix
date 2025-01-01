<script lang="ts">
  import { _ } from "svelte-i18n"

  import { currencies } from "$lib/stores"

  import VirtualListSelect from "$components/LowLevel/VirtualListSelect.svelte"

  interface Props {
    value?: number | null
  }

  let { value = $bindable() }: Props = $props()
</script>

{#if $currencies}
  <VirtualListSelect
    value={$currencies.find(c => c.id === value)}
    items={$currencies}
    placeholder={$_("Currency")}
    label="name"
    oninput={e => (value = e?.detail?.id ?? null)}
  >
    {#snippet selectionSlot(selection)}
      {selection.name} ({selection.code})
    {/snippet}
    {#snippet itemSlot(item)}
      {item.name} ({item.code})
    {/snippet}
  </VirtualListSelect>
{/if}
