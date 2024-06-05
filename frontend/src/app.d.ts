// See https://kit.svelte.dev/docs/types#app

import type createClient from "openapi-fetch"

import type { components, paths } from "$lib/openAPI"

declare global {
  namespace App {
    interface Locals {
      cookie?: string
      locale: string
    }
    interface PageData {
      user: User | null
      apiClient: ReturnType<typeof createClient<paths>>
      countries: components["schemas"]["Country"][]
      regions: components["schemas"]["Region"][]
    }
  }

  // Additional svelte typings (svelte actions)
  // declare namespace svelteHTML {}
}

export {}
