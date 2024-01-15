<script lang="ts">
  // inspiration: https://svelte.dev/examples/modal
  import { createEventDispatcher, onMount } from "svelte"

  const dispatch = createEventDispatcher<{ close: undefined }>()

  export let open = true
  export let dismissible = false

  let dialog: HTMLDialogElement

  function close() {
    if (!dismissible) return
    open = false
    dispatch("close")
  }

  onMount(() => {
    if (dismissible)
      dialog.addEventListener("click", e => {
        const dims = dialog.getBoundingClientRect()
        if (
          e.clientX < dims.left ||
          e.clientX > dims.right ||
          e.clientY < dims.top ||
          e.clientY > dims.bottom
        ) {
          dialog.close() // will call the above close() function implicitly
        }
      })
    if (open) dialog.showModal()
  })

  function modalState(o: boolean) {
    if (!dialog) return
    if (o) dialog.showModal()
    else dialog.close()
  }

  $: modalState(open)
</script>

<dialog
  bind:this={dialog}
  class="rounded border border-gray-300 bg-white p-4 drop-shadow-lg dark:border-gray-800 dark:bg-gray-500 dark:text-white"
  on:close={close}
  on:cancel|preventDefault={close}
>
  <slot />
</dialog>

<style lang="postcss">
  dialog[open] {
    animation: zoom 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
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
  dialog[open]::backdrop {
    animation: fade 0.2s ease-out;
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
