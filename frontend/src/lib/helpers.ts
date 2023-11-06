import { nanoid } from "nanoid"

import type { Obj, ObjVersion } from "$lib/types/generics"
import { DraftStatus, Status } from "$lib/types/generics"
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

export const clickOutside = (
  node: Node,
): {
  update?: (params: unknown) => void
  destroy: () => void
} => {
  const onClick = (event: Event) => {
    if (event.target && !node.contains(event.target as Node)) {
      node.dispatchEvent(new CustomEvent("outClick"))
    }
  }
  document.addEventListener("click", onClick)
  return {
    destroy() {
      document.removeEventListener("click", onClick)
    },
  }
}
