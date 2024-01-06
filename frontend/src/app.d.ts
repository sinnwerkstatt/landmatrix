// See https://kit.svelte.dev/docs/types#app

declare global {
  namespace App {
    interface Locals {
      cookie?: string
      locale: string
    }
  }

  // Additional svelte typings (svelte actions)
  // declare namespace svelteHTML {}
}

export {}
