<script lang="ts">
  export let checked = false
  export let id: string | number
  export let model: "deal" | "investor" = "deal"

  $: modelClasses = model === "deal" ? "text-orange" : "text-pelorous"
  $: normalClasses = "text-gray-700 dark:text-white"
</script>

<div class="flex cursor-pointer items-center gap-1 {$$props.class ?? ''}">
  <label for="{id}-switch" class={!checked ? modelClasses : normalClasses}>
    <slot name="left" />
  </label>
  <input
    id="{id}-switch"
    type="checkbox"
    bind:checked
    on:change|preventDefault
    class={model === "deal" ? "checked:bg-orange" : "checked:bg-pelorous"}
  />
  <label for="{id}-switch" class={checked ? modelClasses : normalClasses}>
    <slot />
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
