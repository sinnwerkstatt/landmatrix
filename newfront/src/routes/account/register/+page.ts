import { redirect } from "@sveltejs/kit";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ parent, url }) => {
  const { user } = await parent();

  if (user?.is_authenticated) throw redirect(301, url.searchParams.get("next") ?? "/");
};
