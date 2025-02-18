<script lang="ts">
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"
  import type { ChangeEventHandler } from "svelte/elements"

  interface Props {
    name: string
    value?: boolean | null
    nullable?: boolean
    wrapperClass?: string
    onchange?: ChangeEventHandler<HTMLInputElement>
  }

  let {
    name,
    value = $bindable(undefined),
    nullable = false,
    wrapperClass = "flex items-center gap-6",
    onchange,
  }: Props = $props()

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
        {name}
        {onchange}
        class={inptClass}
      />
      {$_("Yes")}
    </label>
    <label class={labelClass}>
      <input
        type="radio"
        bind:group={value}
        value={false}
        {name}
        {onchange}
        class={inptClass}
      />
      {$_("No")}
    </label>
    <label class={labelClass}>
      <input
        type="radio"
        bind:group={value}
        value={null}
        {name}
        {onchange}
        class={inptClass}
      />
      {$_("Unknown")}
    </label>
  </div>
{:else}
  <input
    bind:checked={value}
    type="checkbox"
    {name}
    class={inptClass}
    {onchange}
  />
{/if}
