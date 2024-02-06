<script lang="ts">
  import { countries } from "$lib/stores"

  export let value: number | null
</script>

{$countries.find(c => c.id === value)?.name ?? ""}
