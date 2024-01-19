<script lang="ts">
  import { countries } from "$lib/stores"
  import type { Country } from "$lib/types/wagtail"

  export let value: Country | undefined | number
</script>

{$countries.find(c => c.id === (value?.id ?? value))?.name ?? ""}
