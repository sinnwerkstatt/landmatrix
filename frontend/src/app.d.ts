// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
// and what to do when importing types

import type { Client } from "@urql/core"

// https://github.com/sveltejs/kit/discussions/3772#discussioncomment-2131563
declare global {
  namespace App {
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

  namespace svelteHTML {
    interface HTMLAttributes {
      "on:outClick"?: (event: CustomEvent) => void
    }
  }
}

export {}
