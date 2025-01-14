<script lang="ts">
  interface Props {
    value: any
    choices?: { value: string; label: string }[]
    disabled?: boolean
    paddingX?: string
  }

  let {
    value = $bindable(),
    choices = [],
    disabled = false,
    paddingX = "4",
  }: Props = $props()
</script>

<div class="flex flex-col">
  {#each choices as choice}
    <label
      class:disabled
      class="relative grid cursor-pointer grid-rows-1 place-items-center gap-2 hover:bg-a-gray-100 px-{paddingX} py-2"
      style="grid-template-columns: 1rem auto;"
    >
      <!-- Input -->
      <input
        type="radio"
        name={choice.label}
        value={choice.value}
        bind:group={value}
        {disabled}
        class="peer col-start-1 row-start-1 h-4 w-4 appearance-none rounded-2xl border border-a-gray-300 bg-a-gray-50"
      />

      <!-- Checked -->
      <span
        class="pointer-events-none col-start-1 row-start-1 h-2.5 w-2.5 rounded-full bg-a-gray-900 opacity-0 peer-checked:opacity-100"
      ></span>

      <!-- Label -->
      <span class="col-start-2 row-start-1 w-full select-none text-a-sm font-normal">
        {choice.label}
      </span>
    </label>
  {/each}
</div>

<style>
  input {
    @apply cursor-pointer;
  }
  input:checked {
    @apply bg-a-gray-200;
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
  .disabled > input:checked {
    @apply border-a-gray-400 bg-a-gray-400;
  }
</style>
