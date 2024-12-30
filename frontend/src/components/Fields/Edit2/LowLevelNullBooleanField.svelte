<script lang="ts">
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"
  import type { ChangeEventHandler } from "svelte/elements"

  interface Props {
    value?: boolean | null | undefined
    nullable?: boolean
    fieldname?: string | undefined
    wrapperClass?: string
    onchange?: ChangeEventHandler<HTMLInputElement>
  }

  let {
    value = $bindable(undefined),
    nullable = false,
    fieldname = undefined,
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
        name={fieldname}
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
        name={fieldname}
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
        name={fieldname}
        {onchange}
        class={inptClass}
      />
      {$_("Unknown")}
    </label>
  </div>
{:else}
  <input bind:checked={value} type="checkbox" name={fieldname} class={inptClass} />
{/if}
