<script lang="ts">
  import { _ } from "svelte-i18n";
  import Select from "svelte-select";
  import VirtualList from "svelte-tiny-virtual-list";
  import { countries } from "$lib/stores";
  import type { Deal } from "$lib/types/deal";
  import Overlay from "$components/Overlay.svelte";

  export let visible;
  export let deals: Deal[] = [];
  $: dealsCountryIDs = deals?.map((d) => d.country?.id);
  $: relCountries = $countries.filter((c) => dealsCountryIDs.includes(c.id));
</script>

<Overlay bind:visible title={$_("Filter")}>
  <div class="country-filter">
    <Select
      items={relCountries}
      placeholder={$_("Target country")}
      optionIdentifier="id"
      labelIdentifier="name"
      getOptionLabel={(o) => `${o.name} (#${o.id})`}
      getSelectionLabel={(o) => `${o.name} (#${o.id})`}
      showChevron
      {VirtualList}
    />
  </div>
</Overlay>

<style>
  :global(.country-filter .svelte-select, .country-filter .svelte-select + .list) {
    /*height: calc(1.5em + 0.75rem);*/
    --border-radius: 0;
    /*height: 0.2rem;*/
    --input-font-size: 0.6rem;
    /*--selected-item-color: var(--color-orange-600);*/
    --item-is-active-bg: var(--color-lm-orange);
    --item-is-active-color: black;
    /* the following colors are auto-generated via tailwind.config.cjs */
    /*noinspection CssUnresolvedCustomProperty*/
    --border-focus-color: var(--color-orange-600);
    /*noinspection CssUnresolvedCustomProperty*/
    --item-hover-bg: var(--color-orange-100);
  }
</style>
