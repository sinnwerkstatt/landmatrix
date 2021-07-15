export function is_authorized(obj) {
  const u_role = this.$store.state.page.user.role;
  switch (obj.draft_status) {
    case null: // anybody who has a ROLE
      return ["ADMINISTRATOR", "EDITOR", "REPORTER"].includes(u_role);
    case 1: // the Reporter of the Object or Editor,Administrator
      return (
        (obj.revision && obj.revision.user.id === this.$store.state.page.user.id) ||
        ["ADMINISTRATOR", "EDITOR"].includes(u_role)
      );
    case 2: // at least Editor
      return ["ADMINISTRATOR", "EDITOR"].includes(u_role);
    case 3: // only Admins
      return u_role === "ADMINISTRATOR";
    default:
      return false;
  }
}
