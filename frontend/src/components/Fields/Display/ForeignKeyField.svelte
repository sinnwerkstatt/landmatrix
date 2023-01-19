<script lang="ts">
  import { countries } from "$lib/stores"

  import type { FormField } from "$components/Fields/fields"

  type ForeignKey = {
    id: number
    name?: string
    username?: string
  }
  export let formfield: FormField
  export let value: ForeignKey
</script>

<div class="foreignkey_field" data-name={formfield?.name ?? ""}>
  {#if !value || !value.id}
    <!-- no output -->
  {:else if formfield.related_model === "Investor"}
    <a class="investor" target="_blank" rel="noreferrer" href="/investor/{value.id}">
      {value.name} (#{value.id})
    </a>
  {:else if formfield.related_model === "Country"}
    {$countries.find(c => c.id === value.id).name}
  {:else}
    {value.username ?? value.name ?? value.id}
  {/if}
</div>
