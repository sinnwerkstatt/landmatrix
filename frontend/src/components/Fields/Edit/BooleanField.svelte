<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { FormField } from "../fields"

  export let formfield: FormField
  export let value: number
</script>

{#if formfield.class === "NullBooleanField"}
  <div class="space-x-6">
    <label>
      <input type="radio" bind:group={value} value={true} name={formfield.name} />
      {$_("Yes")}
    </label>
    <label>
      <input type="radio" bind:group={value} value={false} name={formfield.name} />
      {$_("No")}
    </label>
    <label>
      <input type="radio" bind:group={value} value={null} name={formfield.name} />
      {$_("Unknown")}
    </label>
  </div>
{:else}
  <input bind:checked={value} type="checkbox" name={formfield.name} />
{/if}
