import store from "$store/index";
import type { Obj } from "$types/generics";

export function is_authorized(obj: Obj): boolean {
  const { id, level } = store.state.user;
  switch (obj.draft_status) {
    case null: // anybody who has a Level
      return level >= 1;
    case 1: // the Reporter of the Object or Editor,Administrator
      return level >= 2 || obj.versions[0]?.created_by?.id === id;
    case 2: // at least Editor
      return level >= 2;
    case 3: // only Admins
      return level === 3;
    default:
      return false;
  }
}
