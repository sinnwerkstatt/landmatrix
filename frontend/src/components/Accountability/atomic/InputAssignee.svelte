<script lang="ts">
  import { createEventDispatcher } from "svelte"

  import { searchMatch } from "$lib/accountability/helpers"
  import { users } from "$lib/accountability/stores"

  import IconSearch from "../icons/IconSearch.svelte"
  import IconXMark from "../icons/IconXMark.svelte"
  import Avatar from "./Avatar.svelte"
  import DropdownMenu from "./DropdownMenu.svelte"

  export let assigneeID: number | undefined = undefined
  export let size: "sm" | "md" = "md"
  export let showOnHover = false
  export let extraClass = "p-2"
  export let disabled = false
  export let auto = true

  let open = false
  let filter = ""

  const dispatch = createEventDispatcher()

  $: assignee = $users.find(u => u.id == assigneeID) ?? undefined

  function selectAssignee(user) {
    if (auto) {
      assigneeID = user.id
    } else {
      dispatch("selectAssignee", { assignee: user.id })
    }
  }

  function unselectAssignee() {
    if (auto) {
      assigneeID = undefined
    } else {
      dispatch("unselectAssignee")
    }
  }
</script>

<div>
  {#if !assignee}
    <button
      class:showOnHover
      class="{extraClass} rounded-lg hover:bg-a-gray-50"
      on:click={() => (open = true)}
    >
      <Avatar {size} label="No assignee" type="assignment" />
    </button>
  {:else}
    <Avatar
      {size}
      label={assignee.name}
      name={assignee.name}
      initials={assignee.initials}
      button={true}
      tooltip={false}
      {extraClass}
      on:click={unselectAssignee}
    />
  {/if}

  {#if open}
    <DropdownMenu extraClass="absolute mt-1 z-20" bind:visible={open}>
      <div class="search m-2">
        <span><IconSearch /></span>
        <input
          {disabled}
          type="text"
          name="name"
          placeholder="Search"
          class="w-full bg-transparent"
          bind:value={filter}
        />
        <button
          {disabled}
          on:click={() => {
            filter = ""
          }}
        >
          <IconXMark />
        </button>
      </div>

      <div class="flex max-h-80 flex-col overflow-auto pb-2">
        {#each $users as user}
          {@const hidden = !searchMatch(user.name, filter)}
          {#if !hidden}
            <button
              class="w-full px-4 py-2 text-left font-normal hover:bg-a-gray-50"
              on:click={() => {
                selectAssignee(user)
                open = false
              }}
            >
              {user.name}
            </button>
          {/if}
        {/each}
      </div>
    </DropdownMenu>
  {/if}
</div>

<style>
  input {
    @apply relative z-0;
    @apply outline-none;
    @apply col-span-2;
  }

  .search {
    @apply h-12;
    @apply min-w-32;
    @apply rounded-lg border px-4 py-2;
    @apply bg-a-gray-50;
    @apply border-a-gray-300;

    display: grid;
    grid-template-columns: 16px auto 16px 16px;
    @apply items-center gap-x-2.5;
  }

  .search > span,
  .search > button {
    @apply text-a-gray-400;
  }

  .search:focus-within {
    @apply border-a-gray-900;
  }

  .search.disabled,
  .search.disabled > span,
  .search.disabled > button {
    @apply text-a-gray-400;
  }

  .search.disabled > button {
    @apply cursor-default;
  }

  .showOnHover {
    @apply opacity-0;
    @apply duration-100;
  }
  .showOnHover:hover {
    @apply opacity-100;
  }
</style>
