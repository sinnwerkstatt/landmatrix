// See https://kit.svelte.dev/docs/types#app

import type { Client } from "openapi-fetch"

import type { Lang } from "$lib/i18n/i18n"
import type { paths } from "$lib/openAPI"
import type { Country, Region, User } from "$lib/types/data"

declare global {
  namespace App {
    interface Locals {
      cookie?: string
      locale: Lang
    }
    interface PageData {
      user: User | null
      apiClient: Client<paths>
      countries: Country[]
      regions: Region[]
    }
  }

  // Additional svelte typings (svelte actions)
  // declare namespace svelteHTML {}
}

export {}
