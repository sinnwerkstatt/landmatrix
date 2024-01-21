<script lang="ts">
  import { dealSections } from "$lib/fieldLookups"

  export let id: string

  $: sec = $dealSections[id]
</script>

<div class="mt-2 space-y-4 pt-6">
  {#if sec.title}
    <h3 class="heading3 my-0">{sec.title}</h3>
  {/if}

  <slot />
</div>
