import { UserRole, type User } from "$lib/types/data"
import {
  isAdmin,
  isAnybodyOrAbove,
  isEditorOrAbove,
  isReporterOrAbove,
} from "$lib/utils/permissions"

describe("User permissions", () => {
  test("isAnybodyOrAbove", () => {
    expect(isAnybodyOrAbove(ANONYMOUS)).toBeFalsy()

    expect(isAnybodyOrAbove(ANYBODY)).toBeTruthy()
    expect(isAnybodyOrAbove(REPORTER)).toBeTruthy()
    expect(isAnybodyOrAbove(EDITOR)).toBeTruthy()
    expect(isAnybodyOrAbove(ADMIN)).toBeTruthy()
  })
  test("isReporterOrAbove", () => {
    expect(isReporterOrAbove(ANONYMOUS)).toBeFalsy()
    expect(isReporterOrAbove(ANYBODY)).toBeFalsy()

    expect(isReporterOrAbove(REPORTER)).toBeTruthy()
    expect(isReporterOrAbove(EDITOR)).toBeTruthy()
    expect(isReporterOrAbove(ADMIN)).toBeTruthy()
  })
  test("isEditorOrAbove", () => {
    expect(isEditorOrAbove(ANONYMOUS)).toBeFalsy()
    expect(isEditorOrAbove(ANYBODY)).toBeFalsy()
    expect(isEditorOrAbove(REPORTER)).toBeFalsy()

    expect(isEditorOrAbove(EDITOR)).toBeTruthy()
    expect(isEditorOrAbove(ADMIN)).toBeTruthy()
  })
  test("isAdmin", () => {
    expect(isAdmin(ANONYMOUS)).toBeFalsy()
    expect(isAdmin(ANYBODY)).toBeFalsy()
    expect(isAdmin(REPORTER)).toBeFalsy()
    expect(isAdmin(EDITOR)).toBeFalsy()

    expect(isAdmin(ADMIN)).toBeTruthy()
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
