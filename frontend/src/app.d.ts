// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
// and what to do when importing types

import type { Client } from "@urql/core"

declare namespace App {
  // interface Errors {}

  interface Locals {
    cookie?: string
    locale: string
  }

  interface PageData {
    urqlClient: Client
  }

  // interface Platform {}
}

export {}
