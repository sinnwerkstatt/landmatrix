<script lang="ts">
  import { dealSections } from "$lib/fieldLookups"
  import { isNotEmpty } from "$lib/helpers"
  import type { DealVersion2 } from "$lib/types/newtypes"

  // export let id: keyof typeof $dealSections
  export let id: string
  export let obj: DealVersion2

  $: sec = $dealSections[id]

  $: sectionEmpty = sec.fields.map(field => obj[field]).filter(isNotEmpty).length === 0
</script>

{#if !sectionEmpty}
  <div class="mt-2 space-y-4">
    <h3 class="heading3 my-0">{sec.title}</h3>

    <slot />
  </div>
{/if}
