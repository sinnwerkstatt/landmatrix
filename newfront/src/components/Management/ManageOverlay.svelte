<script lang="ts">
  import { _ } from "svelte-i18n";
  import type { User } from "$lib/types/user";
  import UserSelect from "$components/Management/UserSelect.svelte";
  import Overlay from "$components/Overlay.svelte";

  export let visible = false;
  export let hideable = true;
  export let title = $_("Submit");

  export let commentInput = false;
  export let commentRequired = false;
  export let comment = "";

  export let assignToUserInput = false;
  export let toUser: User;
  export let showSubmit = true;
  export let cancelButtonTitle = "Cancel";
</script>

<Overlay bind:title bind:hideable bind:visible on:submit>
  <slot />

  {#if commentInput || commentRequired}
    <label class="mb-6 block underline">
      {commentRequired
        ? $_("Please provide a comment explaining your request")
        : $_("Additional comment")}
      <textarea class="mt-1 inpt" bind:value={comment} required={commentRequired} />
    </label>
  {/if}
  {#if assignToUserInput}
    <div class="mb-4">
      <div class="mb-1 block underline">{$_("Assign to user")}</div>
      <UserSelect bind:value={toUser} />
    </div>
  {/if}

  <div slot="footer" class="text-right">
    <button type="button" class="btn btn-cancel" on:click={() => (visible = false)}>
      {cancelButtonTitle}
    </button>
    {#if showSubmit}<button type="submit" class="btn btn-primary">{title}</button>{/if}
  </div>
</Overlay>
