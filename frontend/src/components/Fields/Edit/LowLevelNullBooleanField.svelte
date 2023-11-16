<script lang="ts">
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  export let value: boolean | null | undefined = undefined
  export let nullable = false
  export let fieldname: string | undefined = undefined
  export let wrapperClass = "space-x-6"

  onMount(() => {
    if (value === undefined) value = nullable ? null : false
  })
</script>

{#if nullable}
  <div class={wrapperClass}>
    <label>
      <input type="radio" bind:group={value} value={true} name={fieldname} />
      {$_("Yes")}
    </label>
    <label>
      <input type="radio" bind:group={value} value={false} name={fieldname} />
      {$_("No")}
    </label>
    <label>
      <input type="radio" bind:group={value} value={null} name={fieldname} />
      {$_("Unknown")}
    </label>
  </div>
{:else}
  <input bind:checked={value} type="checkbox" name={fieldname} />
{/if}
