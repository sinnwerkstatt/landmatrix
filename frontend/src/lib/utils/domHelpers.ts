// https://stackoverflow.com/questions/123999
import type { ComponentType } from "svelte"

export const isElementInViewport = (el: HTMLElement): boolean => {
  const rect = el.getBoundingClientRect()

  return (
    rect.top >= 0 &&
    rect.left >= 0 &&
    rect.bottom <=
      (window.innerHeight ||
        document.documentElement.clientHeight) /* or $(window).height() */ &&
    rect.right <=
      (window.innerWidth ||
        document.documentElement.clientWidth) /* or $(window).width() */
  )
}

export const createComponentAsDiv = (
  svelteComponent: ComponentType,
  props: { [key: string]: unknown } = {},
): HTMLDivElement => {
  // if (!document) return null

  const container = document.createElement("div")
  new svelteComponent({ props, target: container })
  return container
}

export const scrollEntryIntoView = (elemId: string | undefined) => {
  if (!elemId) return

  const doScroll = () => {
    const el = document.getElementById(elemId ?? "")
    if (el && !isElementInViewport(el)) {
      el.scrollIntoView({ block: "start", inline: "nearest" })
    }
  }

  // delay a scroll after svelte transitions finished
  setTimeout(doScroll, 300)
}
