<script lang="ts">
  import type { Country } from "$lib/types/wagtail"

  import VirtualListSelect from "./VirtualListSelect.svelte"

  export let countries: Country[] = []
  export let value: Country | undefined = undefined
</script>

<VirtualListSelect bind:value items={countries} label="name" on:input />
