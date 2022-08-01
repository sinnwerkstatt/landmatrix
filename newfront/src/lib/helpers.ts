import { nanoid } from "nanoid";
import type { Obj } from "$lib/types/generics";
import type { User } from "$lib/types/user";
import { UserLevel } from "$lib/types/user";

export function isEmpty(field: unknown): boolean {
  return (
    field === undefined ||
    field === null ||
    field === "" ||
    (Array.isArray(field) && field.length === 0)
  );
}

export function newNanoid(existingIDs: string[] = []): string {
  let newID: string;
  let matching: boolean;
  do {
    newID = nanoid(8);
    matching = existingIDs.includes(newID);
  } while (matching);
  return newID;
}

export function isAuthorized(user: User, obj: Obj): boolean {
  const { id, level } = user;
  switch (obj.draft_status) {
    case null: // anybody who has a relevant role (Reporter, Editor, Admin)
      return level >= UserLevel.REPORTER;
    case 1: // the Reporter of the Object or Editor,Administrator
      return level >= UserLevel.EDITOR || obj.versions[0]?.created_by?.id === id;
    case 2: // at least Editor
      return level >= UserLevel.EDITOR;
    case 3: // only Admins
      return level === UserLevel.ADMINISTRATOR;
    default:
      return false;
  }
}
