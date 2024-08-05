import { error } from "@sveltejs/kit"
import { env } from "$env/dynamic/public"
import createClient from "openapi-fetch"

import {
  allProjects,
  bookmarkedProjects,
  myProjects,
} from "$lib/accountability/projects.js"
import type { components, paths } from "$lib/openAPI"

export async function load({ params, fetch }) {
  const apiClient = createClient<paths>({ baseUrl: env.PUBLIC_BASE_URL, fetch })

  const allProjectsReq = await apiClient.GET("/api/accountability/project/")
  if (allProjectsReq.error) error(500, projectReq.error.detail)
  const allProjectsList: components["schemas"]["Project"] = allProjectsReq.data
  allProjects.set(allProjectsList)

  const myProjectsReq = await apiClient.GET("/api/accountability/project/related/")
  if (myProjectsReq.error) error(500, myProjectsReq.error.detail)
  const myProjectsList: components["schemas"]["Project"] = myProjectsReq.data
  myProjects.set(myProjectsList)

  const bookmarksReq = await apiClient.GET("/api/accountability/project/bookmark/")
  if (bookmarksReq.error) error(500, bookmarksReq.error.detail)
  const bookmarkedProjectsList: components["schemas"]["Project"] = bookmarksReq.data
  bookmarkedProjects.set(bookmarkedProjectsList)

  return {
    allProjects: allProjectsList,
    myProjects: myProjectsList,
    bookmarkedProjects: bookmarkedProjectsList,
  }
}
