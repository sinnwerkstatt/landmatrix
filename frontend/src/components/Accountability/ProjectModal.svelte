<script lang="ts">
  import { goto } from "$app/navigation"
  import { page } from "$app/state"

  import { filters } from "$lib/accountability/filters"
  import { usersToUserChoices } from "$lib/accountability/helpers"
  import {
    createProject,
    deleteProject,
    projectModalData,
    refreshProjects,
    showProjectModal,
    updateProject,
  } from "$lib/accountability/projects"
  import { me, users } from "$lib/accountability/stores"

  import Avatar from "./atomic/Avatar.svelte"
  import Card from "./atomic/Card.svelte"
  import CardTable from "./atomic/CardTable.svelte"
  import Divider from "./atomic/Divider.svelte"
  import Filters from "./atomic/Filters.svelte"
  import Input from "./atomic/Input.svelte"
  import Modal from "./Modal.svelte"

  let userChoices = $derived(
    usersToUserChoices($users).filter(e => e.value != page.data.user.id),
  )

  let disabledModal = $state(false)
  let disabledContent = $state(false)
  let title = $state("")
  let form = $state({
    name: undefined,
    description: undefined,
    editors: [],
  })
  let infos = $state([
    { label: "Created at:", value: undefined },
    { label: "Created by:", value: undefined },
    { label: "Last modification:", value: undefined },
    { label: "Last modification by:", value: undefined },
  ])

  function initModal(data) {
    if (data.action) {
      if (data.action == "create") {
        title = "Create new project"
        form = { name: undefined, description: undefined, editors: [] }
        infos = [
          { label: "Created at:", value: undefined },
          { label: "Created by:", value: undefined },
          { label: "Last modification:", value: undefined },
          { label: "Last modification by:", value: undefined },
        ]
      } else if (data.action == "update") {
        const project = data.project
        title = "Update existing project"
        form = {
          name: project.name,
          description: project.description,
          editors: project.editors,
        }
        infos = [
          {
            label: "Created at:",
            value: new Date(project.created_at).toISOString().substring(0, 10),
          },
          {
            label: "Created by:",
            value: $users.filter(u => u.id == project.owner)[0].name,
          },
          {
            label: "Last modification:",
            value: project.modified_at
              ? new Date(project.modified_at).toISOString().substring(0, 10)
              : undefined,
          },
          { label: "Last modification by:", value: project.modified_by ?? undefined },
        ]
      } else if (data.action == "delete") {
        const project = data.project
        title = "Delete project"
        form = {
          name: project.name,
          description: project.description,
          editors: project.editors,
        }
        infos = [
          {
            label: "Created at:",
            value: new Date(project.created_at).toISOString().substring(0, 10),
          },
          {
            label: "Created by:",
            value: $users.filter(u => u.id == project.owner)[0].name,
          },
          {
            label: "Last modification:",
            value: project.modified_at
              ? new Date(project.modified_at).toISOString().substring(0, 10)
              : undefined,
          },
          { label: "Last modification by:", value: project.modified_by ?? undefined },
        ]
        disabledContent = true
      }
    }
  }
  $effect(() => {
    initModal($projectModalData)
  })

  let formErrors = $state({})
  let formStatus = $derived({
    name: formErrors.name ? "invalid" : "neutral",
    description: formErrors.description ? "invalid" : "neutral",
  })
  $effect(() => {
    if (form) formErrors = {}
  })

  async function save() {
    console.log("=== SAVE CALLED ===")

    formErrors = {}
    disabledModal = true
    disabledContent = true

    if ($projectModalData.action == "create") {
      const res = await createProject(form, $filters)
      if (res.ok) {
        formErrors = {}
        const newProject = await res.json()
        goto(`/accountability/deals/${newProject.id}/`)
        $showProjectModal = false
        try {
          await refreshProjects()
        } catch (error) {
          console.error(error)
        }
      } else {
        formErrors = await res.json()
      }
    } else if ($projectModalData.action == "update") {
      const res = await updateProject($projectModalData.project.id, form, $filters)
      if (res.ok) {
        formErrors = {}
        $showProjectModal = false
        try {
          await refreshProjects()
        } catch (error) {
          console.error(error)
        }
      } else {
        formErrors = await res.json()
      }
    } else if ($projectModalData.action == "delete") {
      const res = await deleteProject($projectModalData.project.id)
      if (res.ok) {
        if (page.params.project == $projectModalData.project.id)
          goto(`/accountability/deals/0/`)
        $showProjectModal = false
        try {
          await refreshProjects()
        } catch (error) {
          console.error(error)
        }
      } else {
        console.error(await res.json())
      }
    }

    disabledModal = false
    disabledContent = false

    // TODO: Show success message or error messages
  }
</script>

<Modal
  bind:open={$showProjectModal}
  {title}
  large={true}
  onclick={save}
  bind:disabled={disabledModal}
>
  {#if $projectModalData.action == "delete"}
    <p class="text-center text-sm text-a-error-500">
      Do you really wish to delete project {$projectModalData.project?.name}? This will
      delete the project for all users. This action cannot be undone.
    </p>
  {/if}

  <div class="grid w-full grid-cols-2 divide-x">
    <div class="pr-4 lg:pr-14">
      <h2 class="text-a-sm font-semibold text-a-gray-500">Informations</h2>
      <Input
        type="text"
        label="Name"
        placeholder="Add name"
        bind:value={form.name}
        status={formStatus.name}
        message={formErrors.name}
        disabled={disabledContent}
      />
      <Input
        type="textarea"
        label="Description"
        placeholder="Add description"
        bind:value={form.description}
        disabled={disabledContent}
        maxlength={280}
        status={formStatus.description}
        message={formErrors.description}
      />
      <Input
        type="multiselect"
        label="Users (who can edit)"
        placeholder="Search for user"
        disabled={disabledContent}
        choices={userChoices}
        bind:value={form.editors}
        badgeType="avatar"
      />
      <Avatar
        initials={$me?.initials}
        label="{$me?.name} (owner)"
        extraClass="mt-1"
        padding={true}
        disabled={disabledContent}
      />
      <Divider />
      <Card>
        <CardTable data={infos} />
      </Card>
    </div>

    <div class="pl-4 lg:pl-14">
      <h2 class="text-a-sm font-semibold text-a-gray-500">Filters</h2>
      <Filters disabled={disabledContent} />
    </div>
  </div>
</Modal>
