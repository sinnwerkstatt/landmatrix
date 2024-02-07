<script lang="ts">
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  export let value: boolean | null | undefined = undefined
  export let nullable = false
  export let fieldname: string | undefined = undefined
  export let wrapperClass = "flex items-center gap-6"

  onMount(() => {
    if (value === undefined) value = nullable ? null : false
  })

  const labelClass = "flex items-center gap-1"
  const inptClass = "h-5 w-5 accent-violet-400"
</script>

{#if nullable}
  <div class={wrapperClass}>
    <label class={labelClass}>
      <input
        type="radio"
        bind:group={value}
        value={true}
        name={fieldname}
        on:change
        class={inptClass}
      />
      {$_("Yes")}
    </label>
    <label class={labelClass}>
      <input
        type="radio"
        bind:group={value}
        value={false}
        name={fieldname}
        on:change
        class={inptClass}
      />
      {$_("No")}
    </label>
    <label class={labelClass}>
      <input
        type="radio"
        bind:group={value}
        value={null}
        name={fieldname}
        on:change
        class={inptClass}
      />
      {$_("Unknown")}
    </label>
  </div>
{:else}
  <input bind:checked={value} type="checkbox" name={fieldname} />
{/if}
