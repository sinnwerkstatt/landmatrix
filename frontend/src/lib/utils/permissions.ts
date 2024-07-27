import { UserRole, type User } from "$lib/types/data"

export const hasRoleOrAbove =
  (role: UserRole) =>
  (user: User | null): boolean =>
    user !== null && user.role >= role

export const isAnybodyOrAbove = hasRoleOrAbove(UserRole.ANYBODY)
export const isReporterOrAbove = hasRoleOrAbove(UserRole.REPORTER)
export const isEditorOrAbove = hasRoleOrAbove(UserRole.EDITOR)
export const isAdmin = hasRoleOrAbove(UserRole.ADMINISTRATOR)
