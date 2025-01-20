import { error } from "@sveltejs/kit"
import { derived, get, writable } from "svelte/store"

import { goto } from "$app/navigation"
import { page } from "$app/stores"

import { getCsrfToken } from "$lib/utils"

import { filters, FilterValues } from "./filters"

// ==============================================================================
// Classes
export class Project {
  id: number = 0
  name: string = ""
  description: string = ""
  owner: object | undefined
  editors: [] = []
  created_at: Date | undefined
  modified_at?: Date
  modified_by?: Date
  filters: FilterValues = new FilterValues()
}

// ==============================================================================
// Stores
export const allProjects = writable([])
export const myProjects = writable([])
export const bookmarkedProjects = writable([])
export const formerProjectID = writable<number | undefined>(-1)

export const bookmarkIds = derived(
  bookmarkedProjects,
  $bookmarkedProjects => {
    return $bookmarkedProjects.length > 0 ? $bookmarkedProjects.map(b => b.id) : []
  },
  [],
)

export const showProjectModal = writable<boolean>(false)
export const projectModalData = writable<{
  action: "create" | "update" | "delete" | undefined
  project?: Project
}>({ action: undefined })

// ==============================================================================
// Project related helper functions
export function updateFilters(project: Project) {
  if (project.id != get(formerProjectID)) {
    if (project.id) {
      const res = new FilterValues(project.filters)
      filters.set(res)
    } else {
      const res = new FilterValues()
      filters.set(res.default())
    }
  }
  formerProjectID.set(project.id)
}

// ==============================================================================
// Functions to communicate with the API
export async function getProject(projectID) {
  // try {
  //   const res = await fetch(`/api/accountability/project/${projectID}/`)
  //   if (!res.ok) throw error(res.status, { message: res.statusText })
  //   return res
  // } catch (err) {
  //   throw err
  // }
  const res = await fetch(`/api/accountability/project/${projectID}/`)
  if (!res.ok) throw error(res.status, { message: res.statusText })
}

export async function fetchAllProjects() {
  try {
    const res = await fetch("/api/accountability/project/")
    const projects = await res.json()
    allProjects.set(projects)
    return projects
  } catch (error) {
    return error
  }
}

export async function fetchMyProjects() {
  try {
    const res = await fetch("/api/accountability/project/related/")
    const projects = await res.json()
    myProjects.set(projects)
    return projects
  } catch (error) {
    return error
  }
}

export async function fetchBookmarkedProjects() {
  try {
    const res = await fetch("/api/accountability/project/bookmark/")
    const projects = await res.json()
    bookmarkedProjects.set(projects)
    return projects
  } catch (error) {
    return error
  }
}

export async function refreshProjects() {
  try {
    await fetchAllProjects()
    await fetchMyProjects()
    await fetchBookmarkedProjects()
  } catch (error) {
    return error
  }
}

export async function addUserBookmark(id) {
  console.log("--- AddUserBookmark ---")
  const project = get(allProjects).find(p => p.id == id)

  console.log("--- Project: ---")
  console.log(project)

  if (project) {
    const order = get(bookmarkedProjects).length + 1
    bookmarkedProjects.set([...get(bookmarkedProjects), project])

    try {
      const res = await fetch("/api/accountability/bookmark/", {
        method: "POST",
        credentials: "include",
        body: JSON.stringify({ project: id, order }),
        headers: {
          "X-CSRFToken": await getCsrfToken(),
          "Content-Type": "application/json",
        },
      })
      const resJSON = await res.json()
      return resJSON
    } catch (error) {
      return error
    }
  } else {
    throw "Project does not exist"
  }
}

export async function removeUserBookmark(id) {
  bookmarkedProjects.set(get(bookmarkedProjects).filter(b => b.id != id))

  try {
    const bookmarkRes = await fetch(`/api/accountability/bookmark`)
    const bookmarks = await bookmarkRes.json()
    const bookmarkId = bookmarks.filter(b => b.project == id)[0].id

    const res = await fetch(`/api/accountability/bookmark/${bookmarkId}/`, {
      method: "DELETE",
      credentials: "include",
      headers: {
        "X-CSRFToken": await getCsrfToken(),
        "Content-Type": "application/json",
      },
    })
    const resJSON = await res.json()
    return resJSON
  } catch (error) {
    return error
  }
}

export async function updateUserBookmarks() {
  const data = get(bookmarkedProjects).map((e, index) => ({
    project: e.id,
    order: index + 1,
  }))

  try {
    const res = await fetch("/api/accountability/bookmark/", {
      method: "PUT",
      credentials: "include",
      body: JSON.stringify(data),
      headers: {
        "X-CSRFToken": await getCsrfToken(),
        "Content-Type": "application/json",
      },
    })
    const resJSON = await res.json()
    return resJSON
  } catch (error) {
    return error
  }
}

export async function createProject(
  form: { name: string; description: string; editors: number[] },
  filters: FilterValues,
) {
  const data = {
    name: form.name,
    description: form.description,
    editors: form.editors,
    filters: Object.assign({}, filters),
  }

  try {
    const res = await fetch("/api/accountability/project/", {
      method: "POST",
      credentials: "include",
      body: JSON.stringify(data),
      headers: {
        "X-CSRFToken": await getCsrfToken(),
        "Content-Type": "application/json",
      },
    })
    return res
  } catch (error) {
    return error
  }
}

export async function updateProject(
  id: number,
  form: { name: string; description: string; editors: number[] },
  filters: FilterValues,
) {
  const data = {
    name: form.name,
    description: form.description,
    editors: form.editors,
    filters: Object.assign({}, filters),
  }

  try {
    const res = await fetch(`/api/accountability/project/${id}/`, {
      method: "PUT",
      credentials: "include",
      body: JSON.stringify(data),
      headers: {
        "X-CSRFToken": await getCsrfToken(),
        "Content-Type": "application/json",
      },
    })
    return res
  } catch (error) {
    return error
  }
}

export async function deleteProject(id: number) {
  try {
    const res = await fetch(`/api/accountability/project/${id}/`, {
      method: "DELETE",
      credentials: "include",
      headers: {
        "X-CSRFToken": await getCsrfToken(),
        "Content-Type": "application/json",
      },
    })
    return res
  } catch (error) {
    return error
  }
}

export function openProjectModal(action: "create" | "update" | "delete", id?: number) {
  if (["update", "delete"].includes(action) && !id) {
    console.error("Project ID must be defined")
  } else if (!["create", "update", "delete"].includes(action)) {
    console.error("Action must be 'create', 'update' or 'delete'")
  } else {
    if (action == "create") {
      projectModalData.set({ action })
      showProjectModal.set(true)
    } else if (action == "update") {
      const currentProject = get(page).params.project
      if (currentProject != id?.toString()) goto(`/accountability/deals/${id}/`) // Load project to edit
      projectModalData.set({
        action,
        project: get(allProjects).filter(p => p.id == id)[0],
      })
      showProjectModal.set(true)
    } else if (action == "delete") {
      projectModalData.set({
        action,
        project: get(allProjects).filter(p => p.id == id)[0],
      })
      showProjectModal.set(true)
    }
  }
}
