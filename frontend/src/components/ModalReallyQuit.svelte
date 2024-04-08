<script lang="ts">
  import { _ } from "svelte-i18n"

  import Modal from "$components/Modal.svelte"

  export let open: boolean
</script>

<Modal bind:open dismissible>
  <h2 class="heading4">{$_("Quit without saving?")}</h2>
  <hr />
  <div class="mb-12 mt-6 text-lg">
    {$_("Do you really want to close the editor?")}
    <br />
    {$_("All unsaved changes will be lost.")}
  </div>
  <div class="flex justify-end gap-4">
    <!-- svelte-ignore a11y-autofocus -->
    <button type="button" class="btn-outline" on:click={() => (open = false)} autofocus>
      Continue editing
    </button>
    <button type="button" class="btn btn-yellow" on:click>Quit without saving</button>
  </div>
</Modal>
