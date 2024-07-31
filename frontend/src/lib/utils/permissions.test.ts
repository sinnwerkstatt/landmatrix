import { UserRole, type User } from "$lib/types/data"
import {
  isAdmin,
  isAnybodyOrAbove,
  isEditorOrAbove,
  isReporterOrAbove,
  isStaff,
} from "$lib/utils/permissions"

describe("User permissions", () => {
  test("isAnybodyOrAbove", () => {
    expect(isAnybodyOrAbove(ANONYMOUS)).toBeFalsy()

    expect(isAnybodyOrAbove(ANYBODY)).toBeTruthy()
    expect(isAnybodyOrAbove(REPORTER)).toBeTruthy()
    expect(isAnybodyOrAbove(EDITOR)).toBeTruthy()
    expect(isAnybodyOrAbove(ADMIN)).toBeTruthy()

    expect(isAnybodyOrAbove(STAFF)).toBeTruthy()
    expect(isAnybodyOrAbove(SUPERUSER)).toBeTruthy()
  })
  test("isReporterOrAbove", () => {
    expect(isReporterOrAbove(ANONYMOUS)).toBeFalsy()
    expect(isReporterOrAbove(ANYBODY)).toBeFalsy()

    expect(isReporterOrAbove(REPORTER)).toBeTruthy()
    expect(isReporterOrAbove(EDITOR)).toBeTruthy()
    expect(isReporterOrAbove(ADMIN)).toBeTruthy()

    expect(isReporterOrAbove(STAFF)).toBeFalsy()
    expect(isReporterOrAbove(SUPERUSER)).toBeTruthy()
  })
  test("isEditorOrAbove", () => {
    expect(isEditorOrAbove(ANONYMOUS)).toBeFalsy()
    expect(isEditorOrAbove(ANYBODY)).toBeFalsy()
    expect(isEditorOrAbove(REPORTER)).toBeFalsy()

    expect(isEditorOrAbove(EDITOR)).toBeTruthy()
    expect(isEditorOrAbove(ADMIN)).toBeTruthy()

    expect(isEditorOrAbove(STAFF)).toBeFalsy()
    expect(isEditorOrAbove(SUPERUSER)).toBeTruthy()
  })
  test("isAdmin", () => {
    expect(isAdmin(ANONYMOUS)).toBeFalsy()
    expect(isAdmin(ANYBODY)).toBeFalsy()
    expect(isAdmin(REPORTER)).toBeFalsy()
    expect(isAdmin(EDITOR)).toBeFalsy()

    expect(isAdmin(ADMIN)).toBeTruthy()

    expect(isAdmin(STAFF)).toBeFalsy()
    expect(isAdmin(SUPERUSER)).toBeTruthy()
  })
  test("isStaff", () => {
    expect(isStaff(ANONYMOUS)).toBeFalsy()
    expect(isStaff(ANYBODY)).toBeFalsy()
    expect(isStaff(REPORTER)).toBeFalsy()
    expect(isStaff(EDITOR)).toBeFalsy()
    expect(isStaff(ADMIN)).toBeFalsy()

    expect(isStaff(STAFF)).toBeTruthy()
    expect(isStaff(SUPERUSER)).toBeTruthy()
  })
})

const ANONYMOUS = null

const ANYBODY = {
  role: UserRole.ANYBODY,
} as User

const EDITOR = {
  role: UserRole.EDITOR,
} as User

const REPORTER = {
  role: UserRole.REPORTER,
} as User

const ADMIN = {
  role: UserRole.ADMINISTRATOR,
} as User

const SUPERUSER = {
  role: UserRole.ANYBODY,
  is_superuser: true,
} as User

const STAFF = {
  role: UserRole.ANYBODY,
  is_staff: true,
} as User
