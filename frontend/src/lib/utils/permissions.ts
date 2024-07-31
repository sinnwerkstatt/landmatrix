import { UserRole, type LeanUser, type User } from "$lib/types/data"

export const hasRoleOrAbove =
  (role: UserRole) =>
  (user: User | LeanUser | null): boolean =>
    user !== null && ((user as User).is_superuser || user.role >= role)

export const isAnybodyOrAbove = hasRoleOrAbove(UserRole.ANYBODY)
export const isReporterOrAbove = hasRoleOrAbove(UserRole.REPORTER)
export const isEditorOrAbove = hasRoleOrAbove(UserRole.EDITOR)
export const isAdmin = hasRoleOrAbove(UserRole.ADMINISTRATOR)

export const isStaff = (user: User | null): boolean =>
  user !== null && (user.is_superuser || user.is_staff)
