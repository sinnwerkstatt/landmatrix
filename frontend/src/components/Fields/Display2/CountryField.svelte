<script lang="ts">
  import { countries } from "$lib/stores"

  export let value: number | null
  export let extras: never
</script>

{$countries.find(c => c.id === value)?.name ?? ""}
