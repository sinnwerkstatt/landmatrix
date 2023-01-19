<script lang="ts">
  import type { FormField } from "$components/Fields/fields"

  type ForeignKey = {
    id: number
    name?: string
    username?: string
  }

  export let formfield: FormField
  export let value: ForeignKey
</script>

<div class="manytomany_field" data-name={formfield?.name ?? ""}>
  {#if formfield.related_model === "Investor"}
    {#each value as val}
      <a class="investor" target="_blank" rel="noreferrer" href="/investor/{value.id}">
        {val.name} (#{val.id})
      </a>
      <br />
    {/each}
  {:else}
    {value}
  {/if}
</div>
