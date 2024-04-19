import { writable } from "svelte/store"

import { browser } from "$app/environment"

import type { BlockImage } from "$lib/types/custom"

export const loading = writable(false)
export const lightboxImage = writable<BlockImage | null>(null)
// export const bindIsDarkModeToPreferredColorScheme = () => {
//   if (sessionStorage.getItem("darkMode")) {
//     console.log("getting session yeay")
//     isDarkMode.set(sessionStorage.getItem("darkMode") === "true")
//   } else if (window.matchMedia) {
//     const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)")
//     isDarkMode.set(mediaQuery.matches)
//     mediaQuery.addEventListener("change", event => {
//       isDarkMode.set(event.matches)
//     })
//   }
// }
export const isMobile = writable<boolean | null>(null)
const TAILWIND_SM_BREAKPOINT_IN_PX = 640
export const bindIsMobileToScreenInnerWidth = () => {
  isMobile.set(window.innerWidth <= TAILWIND_SM_BREAKPOINT_IN_PX)

  window.addEventListener("resize", () => {
    isMobile.set(window.innerWidth <= TAILWIND_SM_BREAKPOINT_IN_PX)
  })
}

if (browser) {
  // bindIsDarkModeToPreferredColorScheme()
  bindIsMobileToScreenInnerWidth()
}

export const contentRootElement = writable<HTMLElement>()

export const isDarkMode = writable(false)
export const toggleDarkMode = () => {
  if (document.documentElement.classList.contains("dark")) {
    isDarkMode.set(false)
    sessionStorage.setItem("theme", "light")
    document.documentElement.classList.remove("dark")
  } else {
    isDarkMode.set(true)
    sessionStorage.setItem("theme", "dark")
    document.documentElement.classList.add("dark")
  }
}
