<script lang="ts">
  import { createEventDispatcher } from "svelte"
  import { _ } from "svelte-i18n"

  import type { User } from "$lib/types/user"

  import UserSelect from "$components/Management/UserSelect.svelte"
  import Overlay from "$components/Overlay.svelte"

  const dispatch = createEventDispatcher()

  export let visible = false
  export let hideable = true
  export let title = $_("Submit")

  export let commentInput = false
  export let commentRequired = false

  let comment = ""

  export let assignToUserInput = false
  export let toUser: User | null = null
  export let showSubmit = true

  const onSubmit = async () => {
    dispatch("submit", { comment, toUser })
    comment = ""
  }
</script>

<Overlay
  bind:title
  bind:hideable
  bind:visible
  on:submit={onSubmit}
  on:close
  {showSubmit}
>
  <slot />

  {#if commentInput || commentRequired}
    <label class="mb-6 block underline">
      {commentRequired
        ? $_("Please provide a comment explaining your request")
        : $_("Additional comment")}
      <textarea class="inpt mt-1" bind:value={comment} required={commentRequired} />
    </label>
  {/if}
  {#if assignToUserInput}
    <div class="mb-4">
      <div class="mb-1 block underline">{$_("Assign to user")}</div>
      <UserSelect bind:value={toUser} />
    </div>
  {/if}
</Overlay>
