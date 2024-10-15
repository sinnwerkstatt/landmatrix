<script lang="ts">
  import { _ } from "svelte-i18n"

  type Model = "deal" | "investor"

  export let model: Model

  let models: { value: Model; label: string }[]
  $: models = [
    { value: "deal", label: $_("Deals") },
    { value: "investor", label: $_("Investors") },
  ]
</script>

<div class="flex h-fit gap-4">
  <span class="italic after:content-[':']">
    {$_("Show quality indicators for")}
  </span>
  {#each models as { value, label }}
    <button
      class="model-switcher border-b px-1 font-bold hover:bg-gray-50 dark:hover:bg-gray-700"
      class:deal={value === "deal"}
      class:investor={value === "investor"}
      class:is-active={value === model}
      on:click={() => (model = value)}
      type="button"
    >
      {label}
    </button>
  {/each}
</div>

<style lang="postcss">
  .model-switcher {
    @apply text-gray-600 dark:text-white;
  }
  .model-switcher.deal {
    @apply hover:border-orange hover:text-orange;
  }
  .model-switcher.deal.is-active {
    @apply border-orange text-orange;
  }
  .model-switcher.investor {
    @apply hover:border-pelorous hover:text-pelorous;
  }
  .model-switcher.investor.is-active {
    @apply border-pelorous text-pelorous;
  }
</style>
