<script lang="ts">
  import type { Snippet } from "svelte"
  import type { ChangeEventHandler } from "svelte/elements"

  interface Props {
    checked?: boolean
    id: string | number
    model?: "deal" | "investor"
    class?: string
    left?: Snippet
    children?: Snippet
    onchange?: ChangeEventHandler<HTMLInputElement>
  }

  let {
    checked = $bindable(false),
    id,
    model = "deal",
    class: className = "",
    left,
    children,
    onchange,
  }: Props = $props()

  let modelClasses = $derived(model === "deal" ? "text-orange" : "text-pelorous")
  let normalClasses = $derived("text-gray-700 dark:text-white")
</script>

<div class="flex cursor-pointer items-center gap-1 {className}">
  <label for="{id}-switch" class={!checked ? modelClasses : normalClasses}>
    {@render left?.()}
  </label>
  <input
    id="{id}-switch"
    type="checkbox"
    bind:checked
    {onchange}
    class={model === "deal" ? "checked:bg-orange" : "checked:bg-pelorous"}
  />
  <label for="{id}-switch" class={checked ? modelClasses : normalClasses}>
    {@render children?.()}
  </label>
</div>

<style lang="postcss">
  input {
    @apply bg-gray-100;
    appearance: none;
    margin: 0;
    display: grid;
    place-content: center;
    width: 2.25em;
    height: 1.25em;
    transition: background-color 100ms ease-in-out;
    cursor: pointer;
  }

  input::before {
    content: "";
    width: 1em;
    height: 1em;
    transform: translateX(-50%);
    transition: 100ms transform ease-in-out;
    box-shadow: inset 1.15em 1.15em white;
    cursor: pointer;
  }

  input:checked::before {
    transform: translateX(50%);
  }
</style>
