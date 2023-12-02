// See https://kit.svelte.dev/docs/types#app

import type { Client } from "@urql/core"

declare global {
  namespace App {
    interface Locals {
      cookie?: string
      locale: string
    }

    interface PageData {
      urqlClient: Client
    }
  }

  // Additional svelte typings (svelte actions)
  // declare namespace svelteHTML {}
}

export {}
