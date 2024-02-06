<script lang="ts">
  import { _ } from "svelte-i18n"

  import TrashIcon from "$components/icons/TrashIcon.svelte"

  export let disabled = false
</script>

<div class="mt-3 text-right">
  <button type="button" {disabled} on:click title={$_("Remove entry")}>
    <TrashIcon class="h-5 w-5 {!disabled ? 'text-red-600' : 'text-gray-200'}" />
  </button>
</div>
