<script lang="ts">
  import {
    addUserBookmark,
    allProjects,
    // openProjectModal,
    removeUserBookmark,
  } from "$lib/accountability/projects"
  import { users } from "$lib/accountability/stores"

  import Modal from "$components/Accountability/Modal.svelte"

  import Input from "./atomic/Input.svelte"
  import Pagination from "./atomic/Pagination.svelte"
  import Section from "./atomic/Section.svelte"
  import SidebarTab from "./atomic/SidebarTab.svelte"

  // import Button from "./Button.svelte"
  // import IconFilter from "./icons/IconFilter.svelte"

  // Open modal to filter projects
  let openModal = $state(false)

  // Alphabetically sort projects
  let sortedProjects = $state([])
  $effect(() => {
    sortedProjects = $allProjects.sort((a, b) => a.name.localeCompare(b.name))
  })

  // Bind page content from Pagination
  let pageContent = $state([])

  // Swap alphabetical sorting each time the button is clicked
  function sortProjects() {
    sortedProjects = sortedProjects.reverse()
  }

  // Menu - TMP, uncomment functions later when they are ready
  function handleEdit() {
    // const projectId = event.detail.id
    // console.log("Edit action: " + projectId)
  }

  function handleDelete() {
    // openProjectModal('delete', event.detail.id)
  }

  async function handleBookmark(projectId: number, action: string) {
    if (action == "add") {
      try {
        await addUserBookmark(projectId)
      } catch (error) {
        console.error(error)
      }
    } else if (action == "remove") {
      try {
        await removeUserBookmark(projectId)
      } catch (error) {
        console.error(error)
      }
    }
  }
</script>

<div class="my-2 flex h-full flex-col overflow-hidden">
  <!-- <Button
    label="Filter projects (0)"
    type="outline"
    style="neutral"
    tailwind="self-center"
    on:click={() => (openModal = true)}
  >
    <span slot="iconAfter"><IconFilter /></span>
  </Button> -->

  <div class="h-full overflow-scroll">
    <Section
      title="Results"
      alwaysOpen={true}
      sortable="auto"
      stickyTitle={true}
      onSort={sortProjects}
    >
      <Pagination bind:dataset={sortedProjects} bind:pageContent rowHeight="56">
        {#each pageContent as { id, name }}
          <SidebarTab
            {id}
            label={name}
            menu={true}
            handle={false}
            onEdit={handleEdit}
            onBookmark={handleBookmark}
            onDelete={handleDelete}
          />
        {/each}
      </Pagination>
    </Section>
  </div>
</div>

<Modal
  bind:open={openModal}
  title="Filter projects"
  confirmLabel="Filter"
  extraClass="overflow-visible"
>
  <div class="h-fit">
    <Input type="text" label="Name" placeholder="Name" icon="search" />
    <Input type="text" label="Description" placeholder="Description" icon="search" />
    <Input
      type="select"
      label="Project creator"
      placeholder="Search for user"
      choices={$users}
    />
  </div>
</Modal>
