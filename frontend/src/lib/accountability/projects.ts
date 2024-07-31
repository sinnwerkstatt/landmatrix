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
