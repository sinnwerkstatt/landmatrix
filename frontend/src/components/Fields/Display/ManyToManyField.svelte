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

{#if formfield.related_model === "Investor"}
  <ul>
    {#each value as val}
      <li>
        <a
          class="investor"
          target="_blank"
          rel="noreferrer"
          href="/investor/{value.id}"
        >
          {val.name} (#{val.id})
        </a>
      </li>
    {/each}
  </ul>
{:else}
  {value}
{/if}
