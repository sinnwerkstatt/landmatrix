import { nanoid } from "nanoid"
import type { ActionReturn } from "svelte/action"

import type { Obj, ObjVersion } from "$lib/types/generics"
import { DraftStatus, Status } from "$lib/types/generics"
import { Version2Status, type DealHull, type InvestorHull } from "$lib/types/newtypes"
import type { User } from "$lib/types/user"
import { UserRole } from "$lib/types/user"

export function isEmpty(field: unknown): boolean {
  return (
    field === undefined ||
    field === null ||
    field === "" ||
    (Array.isArray(field) && field.length === 0)
  )
}

export function newNanoid(existingIDs: string[] = []): string {
  let newID: string
  let matching: boolean
  do {
    newID = nanoid(8)
    matching = existingIDs.includes(newID)
  } while (matching)
  return newID
}

export const findActiveVersion = (
  object: Obj,
  otype: "deal" | "investor",
): ObjVersion | undefined =>
  object.versions.find(version => {
    const status = (version[otype] as Obj).status
    const draftStatus = (version[otype] as Obj).draft_status
    return (status === Status.LIVE || status === Status.UPDATED) && draftStatus === null
  })

export const isCreator = (user: User, obj: Obj | ObjVersion): boolean =>
  user.id === obj.created_by?.id
export const isEditorPlus = (user: User): boolean => user.role >= UserRole.EDITOR
export const isAdmin = (user: User): boolean => user.role >= UserRole.ADMINISTRATOR

export function isAuthorized(user: User, obj: Obj): boolean {
  const { role } = user
  switch (obj.draft_status) {
    case null: // anybody who has a relevant role (Reporter, Editor, Admin)
      return role >= UserRole.REPORTER
    case DraftStatus.DRAFT: // the Reporter of the Object or Editor,Administrator
      return role >= UserRole.EDITOR || isCreator(user, obj.versions[0])
    case DraftStatus.REVIEW: // at least Editor
      return role >= UserRole.EDITOR
    case DraftStatus.REJECTED: // only Admins
      return role === UserRole.ADMINISTRATOR
    case DraftStatus.ACTIVATION: // only Admins
      return role === UserRole.ADMINISTRATOR
    default:
      return false
  }
}

export function newIsAuthorized(user: User, obj: DealHull | InvestorHull): boolean {
  const { role } = user
  switch (obj.selected_version.status) {
    case null: // anybody who has a relevant role (Reporter, Editor, Admin)
      return role >= UserRole.REPORTER
    case Version2Status.DRAFT: // the Reporter of the Object or Editor,Administrator
      return role >= UserRole.EDITOR || user.id === obj.selected_version.created_by_id
    case Version2Status.REVIEW: // at least Editor
      return role >= UserRole.EDITOR
    case Version2Status.REJECTED: // only Admins
      return role === UserRole.ADMINISTRATOR
    case Version2Status.ACTIVATION: // only Admins
      return role === UserRole.ADMINISTRATOR
    default:
      return false
  }
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
