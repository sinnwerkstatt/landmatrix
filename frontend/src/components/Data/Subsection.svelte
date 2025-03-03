<script lang="ts">
  import type { Snippet } from "svelte"

  import { isNotEmpty } from "$lib/helpers"
  import { objectSections } from "$lib/sections"
  import type { DealVersion, InvestorVersion } from "$lib/types/data"

  interface Props {
    // todo marcus maybe?
    // export let id: keyof typeof $dealSections
    id: string
    obj: DealVersion | InvestorVersion
    children?: Snippet
  }

  let { id, obj, children }: Props = $props()

  let sec = $derived($objectSections[id])

  let sectionEmpty = $derived(
    sec.fields.map(field => obj[field]).filter(isNotEmpty).length === 0,
  )
</script>

{#if !sectionEmpty}
  <div class="mt-8 space-y-4 first:mt-2">
    <h3 class="heading4 my-0">{sec.title}</h3>

    {@render children?.()}
  </div>
{/if}
