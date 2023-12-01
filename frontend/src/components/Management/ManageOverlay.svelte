<script lang="ts">
  import { createEventDispatcher, onDestroy, onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { allUsers } from "$lib/stores"
  import type { User } from "$lib/types/user"
  import { UserRole } from "$lib/types/user"

  import UserSelect from "$components/LowLevel/UserSelect.svelte"
  import Overlay from "$components/Overlay.svelte"

  const dispatch = createEventDispatcher()

  export let visible = false
  export let hideable = true
  export let title = $_("Submit")

  export let commentInput = false
  export let commentRequired = false

  export let comment = ""

  export let assignToUserInput = false
  export let toUser: User | number | undefined = undefined
  export let toUserRequired = false
  export let extraUserIDs: number[] = []
  export let showSubmit = true
  export let submitTitle: string | null = null

  const onSubmit = async e => {
    const form = e.target as HTMLFormElement
    if (!form.checkValidity()) form.reportValidity()

    dispatch("submit", { comment, toUser })
  }

  onMount(() => {
    if (typeof toUser === "number") {
      toUser = $allUsers.find(u => u.id === toUser)
    }
  })
  onDestroy(() => (comment = ""))

  let users: User[]
  $: users = $allUsers.filter(
    u => extraUserIDs.includes(u.id) || u.role > UserRole.REPORTER,
  )
</script>

<Overlay
  bind:title
  bind:hideable
  bind:visible
  bind:submitTitle
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
      <UserSelect bind:value={toUser} {users} required={toUserRequired} />
    </div>
  {/if}
</Overlay>
