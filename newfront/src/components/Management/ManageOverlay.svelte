<script lang="ts">
  import { gql } from "@apollo/client/core";
  import { _ } from "svelte-i18n";
  import Select from "svelte-select";
  import { writable } from "svelte/store";
  import { page } from "$app/stores";
  import type { User } from "$lib/types/user";
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

  let users = writable<User[]>(undefined);

  async function fetchUsers() {
    if ($users !== undefined) return;
    const { data } = await $page.stuff.secureApolloClient.query<{ users: User[] }>({
      query: gql`
        {
          users {
            id
            full_name
            username
          }
        }
      `,
    });
    users.set([...data.users].sort((a, b) => a.full_name.localeCompare(b.full_name)));
  }
  fetchUsers();
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
      <Select
        items={$users}
        bind:value={toUser}
        placeholder={$_("User")}
        optionIdentifier="id"
        getOptionLabel={(o) => `${o.full_name} (<b>${o.username}</b>)`}
        getSelectionLabel={(o) => `${o.full_name} (<b>${o.username}</b>)`}
        showChevron
      />
    </div>
  {/if}

  <div slot="footer" class="text-right">
    <button type="button" class="btn btn-cancel" on:click={() => (visible = false)}>
      {cancelButtonTitle}
    </button>
    {#if showSubmit}<button type="submit" class="btn btn-primary">{title}</button>{/if}
  </div>
</Overlay>
