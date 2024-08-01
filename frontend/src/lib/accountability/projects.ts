import { get } from "svelte/store"

import { getCsrfToken } from "$lib/utils"

import { allProjects, bookmarkedProjects, myProjects } from "./stores"

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

export async function updateUserBookmarks() {
  console.log("============= PUT =============")
  const bookmarks = get(bookmarkedProjects).map(e => e.id)

  console.log(JSON.stringify({ bookmarks: bookmarks }))

  try {
    const res = await fetch("/api/accountability/user/me/", {
      method: "PUT",
      credentials: "include",
      body: JSON.stringify({ bookmarks: bookmarks }),
      headers: {
        "X-CSRFToken": await getCsrfToken(),
        "Content-Type": "application/json",
      },
    })
    console.log(res)
    const resJSON = await res.json()
    console.log(resJSON.bookmarks)
    return resJSON
  } catch (error) {
    console.error(error)
    return error
  }
}
