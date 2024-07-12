// See https://kit.svelte.dev/docs/types#app

import type createClient from "openapi-fetch"

import type { paths } from "$lib/openAPI"
import type { Country, Region, User } from "$lib/types/data"

declare global {
  namespace App {
    interface Locals {
      cookie?: string
      locale: string
    }
    interface PageData {
      user: User | null
      apiClient: ReturnType<typeof createClient<paths>>
      countries: Country[]
      regions: Region[]
    }
  }

  // Additional svelte typings (svelte actions)
  // declare namespace svelteHTML {}
}

export {}
