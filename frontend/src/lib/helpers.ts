import { nanoid } from "nanoid"
import type { ActionReturn } from "svelte/action"

// What about objects?
export const isNotEmpty = (field: unknown): boolean =>
  !(field === undefined || field === null || field === "") &&
  !(Array.isArray(field) && field.length === 0)

export function newNanoid(existingIDs: string[] = []): string {
  let newID: string
  let matching: boolean
  do {
    newID = nanoid(8)
    matching = existingIDs.includes(newID)
  } while (matching)
  return newID
}

interface ClickOutsideAttributes {
  "on:outClick": (e: CustomEvent) => void
}

export const clickOutside = (
  node: HTMLElement,
): ActionReturn<undefined, ClickOutsideAttributes> => {
  const onClick = (event: Event): void => {
    if (event.target && !node.contains(event.target as HTMLElement)) {
      node.dispatchEvent(new CustomEvent("outClick"))
    }
  }
  document.addEventListener("click", onClick)
  return {
    destroy(): void {
      document.removeEventListener("click", onClick)
    },
  }
}
