<script lang="ts">
  import Avatar from "$components/Accountability/atomic/Avatar.svelte"
  import NavbarItem from "$components/Accountability/atomic/NavbarItem.svelte"
  import IconList from "$components/Accountability/icons/IconList.svelte"
  // import IconToDo from "$components/Accountability/icons/IconToDo.svelte"
  // import IconDocs from "$components/Accountability/icons/IconDocs.svelte"
  import Logo from "$components/Accountability/icons/Logo.svelte"
</script>

<div
  class="flex h-full flex-col flex-nowrap items-center justify-between border border-a-gray-200 bg-white py-6"
>
  <!-- Top section -->
  <div class="flex flex-col items-center">
    <Logo />
    <div class="mt-10 flex flex-col flex-nowrap gap-4 px-6">
      <NavbarItem label="Deals" href="/accountability/deals/">
        <span slot="icon"><IconList /></span>
      </NavbarItem>
      <!-- <NavbarItem label="To Do" href="/accountability/todo/">
        <span slot="icon"><IconToDo /></span>
      </NavbarItem>
      <NavbarItem label="Doc" href="/accountability/doc/">
        <span slot="icon"><IconDocs /></span>
      </NavbarItem> -->
    </div>
  </div>

  <!-- Bottom section -->
  <div>
    <Avatar />
  </div>
</div>
