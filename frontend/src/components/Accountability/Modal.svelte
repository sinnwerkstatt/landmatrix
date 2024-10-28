<script lang="ts">
  import { fade } from "svelte/transition"

  import Button from "./Button.svelte"
  import IconXMark from "./icons/IconXMark.svelte"

  export let open: boolean = false
  export let extraClass: string = ""
  export let title: string
  export const large: boolean = false
  export let confirmLabel = "Save"
  export let disabled = false
</script>

{#if open}
  <div
    class="absolute left-0 top-0 z-30 grid h-screen w-screen place-items-center bg-a-gray-900/50 md:p-12"
    transition:fade={{ duration: 100 }}
  >
    <div
      class="relative flex max-h-full max-h-full min-w-[30rem] flex-col overflow-hidden rounded-lg bg-white shadow-a-md {extraClass} w-full md:w-10/12 lg:w-8/12 2xl:w-1/2"
    >
      <div class="header border-b text-center text-a-xl font-semibold">
        {title}
        <button
          class="absolute right-4 top-4 text-a-gray-400"
          {disabled}
          on:click={() => (open = false)}
        >
          <IconXMark size="24" />
        </button>
      </div>
      <div class="overflow-auto px-14 py-4">
        <slot />
      </div>
      <div class="footer flex justify-center gap-4 border-t">
        <Button
          label="Cancel"
          style="neutral"
          type="outline"
          {disabled}
          on:click={() => (open = false)}
        />
        <Button label={confirmLabel} style="neutral" {disabled} on:click />
      </div>
    </div>
  </div>
{/if}

<style>
  .header,
  .footer {
    @apply w-full p-6;
  }

</style>
