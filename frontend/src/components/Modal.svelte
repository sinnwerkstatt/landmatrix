<script lang="ts">
  // inspiration: https://svelte.dev/examples/modal
  import { onMount, type Snippet } from "svelte"
  import { twMerge } from "tailwind-merge"

  interface Props {
    open: boolean
    dismissible?: boolean
    class?: string
    style?: string
    children?: Snippet
    onclose?: () => void
  }

  let {
    open = $bindable(),
    dismissible = false,
    class: className = "",
    style = "",
    children,
    onclose,
  }: Props = $props()
  let dialog: HTMLDialogElement | undefined = $state()

  function close() {
    if (!dismissible) return
    open = false
    onclose?.()
  }

  onMount(() => {
    if (!dialog) return
    if (dismissible)
      dialog.addEventListener("click", e => {
        const dims = dialog!.getBoundingClientRect()
        if (
          e.clientX < dims.left ||
          e.clientX > dims.right ||
          e.clientY < dims.top ||
          e.clientY > dims.bottom
        ) {
          dialog!.close() // will call the above close() function implicitly
        }
      })
    if (open) dialog.showModal()
  })

  function modalState(o: boolean) {
    if (!dialog) return
    if (o) dialog.showModal()
    else dialog.close()
  }

  $effect(() => {
    modalState(open)
  })
</script>

<dialog
  bind:this={dialog}
  class={twMerge(
    "rounded border border-gray-300 bg-white p-4 drop-shadow-lg dark:border-gray-600 dark:bg-gray-900 dark:text-white",
    className,
  )}
  {style}
  onclose={close}
>
  {@render children?.()}
</dialog>

<style lang="postcss">
  dialog {
    --open-speed: 300ms;
  }
  dialog[open] {
    animation: zoom var(--open-speed) cubic-bezier(0.34, 1.56, 0.64, 1);
  }
  @keyframes zoom {
    from {
      transform: scale(0.85);
    }
    to {
      transform: scale(1);
    }
  }
  dialog::backdrop {
    @apply bg-black/20;
    backdrop-filter: blur(1px);
  }
  :global(.dark dialog::backdrop) {
    /*@apply bg-white/20;*/
    @apply bg-black/80;
  }
  dialog[open]::backdrop {
    animation: fade var(--open-speed) ease-out;
  }
  @keyframes fade {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }
</style>
