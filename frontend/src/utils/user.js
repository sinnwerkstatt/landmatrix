export function is_authorized(obj) {
  const { id, role } = this.$store.state.page.user;
  switch (obj.draft_status) {
    case null: // anybody who has a ROLE
      return ["ADMINISTRATOR", "EDITOR", "REPORTER"].includes(role);
    case 1: // the Reporter of the Object or Editor,Administrator
      return (
        ["ADMINISTRATOR", "EDITOR"].includes(role) || obj.revision?.user?.id === id
      );
    case 2: // at least Editor
      return ["ADMINISTRATOR", "EDITOR"].includes(role);
    case 3: // only Admins
      return role === "ADMINISTRATOR";
    default:
      return false;
  }
}
