import store from "$store/index";
import type { Obj } from "$types/generics";

export function is_authorized(obj: Obj): boolean {
  const { id, role } = store.state.user;
  switch (obj.draft_status) {
    case null: // anybody who has a Role
      return role >= 1;
    case 1: // the Reporter of the Object or Editor,Administrator
      return role >= 2 || obj.versions[0]?.created_by?.id === id;
    case 2: // at least Editor
      return role >= 2;
    case 3: // only Admins
      return role === 3;
    default:
      return false;
  }
}
