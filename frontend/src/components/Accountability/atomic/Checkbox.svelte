<script lang="ts">
  import IconCheck from "../icons/IconCheck.svelte"
  import IconMinus from "../icons/IconMinus.svelte"

  interface Props {
    value?: string
    checked?: boolean
    partiallyChecked?: boolean
    label?: string
    bold?: boolean
    disabled?: boolean
    hidden?: boolean
    paddingX?: string
    paddingY?: string
    onchanged?: (value: string, checked: boolean) => void
  }

  let {
    value = "",
    checked = $bindable(false),
    partiallyChecked = $bindable(false),
    label = "",
    bold = false,
    disabled = false,
    hidden = false,
    paddingX = "4",
    paddingY = "2",
    onchanged,
  }: Props = $props()
</script>

<label
  class:disabled
  class:hidden
  class="relative grid h-fit cursor-pointer grid-rows-1 place-items-center hover:bg-a-gray-100 px-{paddingX} py-{paddingY}"
  style="grid-template-columns: 1rem auto;"
>
  <!-- Checkbox -->
  <input
    type="checkbox"
    name="input"
    {value}
    bind:checked
    onchange={() => onchanged?.(value, checked)}
    {disabled}
    class="col-start-1 row-start-1 h-4 w-4 appearance-none rounded border border-a-gray-300 bg-a-gray-50"
    class:partiallyChecked
  />

  <!-- Checked svg -->
  <span class="pointer-events-none z-10 col-start-1 row-start-1 text-a-gray-50">
    {#if checked}
      <IconCheck />
    {:else if partiallyChecked}
      <IconMinus size="16" />
    {/if}
  </span>

  <!-- Label -->
  {#if label}
    <span
      class="col-start-2 row-start-1 w-full select-none pl-2 text-a-sm font-normal"
      class:bold
    >
      {label}
    </span>
  {/if}
</label>

<style>
  .bold {
    @apply font-semibold;
  }

  .partiallyChecked {
    @apply border-a-gray-400;
    @apply bg-a-gray-400;
  }

  input {
    @apply cursor-pointer;
  }
  input:checked {
    @apply border-a-gray-900;
    @apply bg-a-gray-900;
  }

  .disabled {
    @apply cursor-default;
    @apply text-a-gray-400;
  }
  .disabled:hover {
    @apply bg-white;
  }
  .disabled > input {
    @apply cursor-default;
  }
  .disabled > input:checked,
  .disabled > input.partiallyChecked {
    @apply border-a-gray-400 bg-a-gray-400;
  }
</style>
