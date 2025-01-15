<script lang="ts">
  import {
    addUserBookmark,
    bookmarkedProjects,
    myProjects,
    openProjectModal,
    removeUserBookmark,
    updateUserBookmarks,
  } from "$lib/accountability/projects"

  import Section from "./atomic/Section.svelte"
  import SidebarTab from "./atomic/SidebarTab.svelte"
  import SortableList from "./atomic/SortableList.svelte"

  function handleEdit(id) {
    openProjectModal("update", id)
  }

  function handleDelete(id) {
    openProjectModal("delete", id)
  }

  async function handleBookmark(id, action) {
    if (action == "add") {
      try {
        await addUserBookmark(id)
      } catch (error) {
        console.error(error)
      }
    } else if (action == "remove") {
      try {
        await removeUserBookmark(id)
      } catch (error) {
        console.error(error)
      }
    }
  }

  async function handleReorder() {
    try {
      await updateUserBookmarks()
    } catch (error) {
      console.error(error)
    }
  }
</script>

<div class="flex h-fit flex-col overflow-hidden">
  <SidebarTab label="All deals" active={true} />

  <div class="overflow-auto">
    <Section title="Bookmarked projects" onEdit onBookmark>
      <SortableList
        bind:items={$bookmarkedProjects}
        onEdit={handleEdit}
        onBookmark={handleBookmark}
        onReorder={handleReorder}
        onDelete={handleDelete}
      />
    </Section>

    <Section title="My projects">
      {#each $myProjects as { id, name }, i}
        {@const menuPosition = i + 1 == $myProjects.length ? "top" : "bottom"}
        <SidebarTab
          {id}
          label={name}
          menu={true}
          handle={false}
          onEdit={handleEdit}
          onBookmark={handleBookmark}
          onDelete={handleDelete}
          {menuPosition}
        />
      {/each}
    </Section>
  </div>
</div>
