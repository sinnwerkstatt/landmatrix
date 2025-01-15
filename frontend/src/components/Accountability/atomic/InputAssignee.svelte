<script lang="ts">
  import { searchMatch } from "$lib/accountability/helpers"
  import { users } from "$lib/accountability/stores"

  import IconSearch from "../icons/IconSearch.svelte"
  import IconXMark from "../icons/IconXMark.svelte"
  import Avatar from "./Avatar.svelte"
  import DropdownMenu from "./DropdownMenu.svelte"

  interface Props {
    assigneeID?: number | undefined
    size?: "sm" | "md"
    showOnHover?: boolean
    extraClass?: string
    disabled?: boolean
    auto?: boolean
    selectAssignee?: (user: { id: number }) => void
    unselectAssignee?: () => void
  }

  let {
    assigneeID = $bindable(undefined),
    size = "md",
    showOnHover = false,
    extraClass = "p-2",
    disabled = false,
    auto = true,
    selectAssignee,
    unselectAssignee,
  }: Props = $props()

  let open = $state(false)
  let filter = $state("")

  let top = $state(200)
  let left = $state(200)

  let assignee = $derived($users.find(u => u.id == assigneeID) ?? undefined)

  function selectAssigneeFunc(user) {
    if (auto) {
      assigneeID = user.id
    } else {
      selectAssignee(user.id)
    }
  }

  // function unselectAssigneeFunc() {
  //   if (auto) {
  //     assigneeID = undefined
  //   } else {
  //     unselectAssignee()
  //   }
  // }

  function showDropdown(
    event: MouseEvent & { currentTarget: EventTarget & HTMLButtonElement },
  ) {
    open = true
    top = event.clientY + 16
    left = event.clientX + 16 - 200
  }
</script>

<div>
  {#if !assignee}
    <button
      class:showOnHover
      class="{extraClass} rounded-lg hover:bg-a-gray-50"
      onclick={event => showDropdown(event)}
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
      onclick={unselectAssignee}
    />
  {/if}

  {#if open}
    <DropdownMenu
      extraClass="absolute mt-1 z-20"
      bind:visible={open}
      bind:top
      bind:left
    >
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
          onclick={() => {
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
              onclick={() => {
                selectAssigneeFunc(user)
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

  /* .search.disabled > span, */
  /* .search.disabled > button, */
  .search.disabled {
    @apply text-a-gray-400;
  }

  /* .search.disabled > button {
    @apply cursor-default;
  } */

  .showOnHover {
    @apply opacity-0;
    @apply duration-100;
  }
  .showOnHover:hover {
    @apply opacity-100;
  }
</style>
