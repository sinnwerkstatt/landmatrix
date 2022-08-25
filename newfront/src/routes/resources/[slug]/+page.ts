import { pageQuery } from "$lib/queries";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ url, fetch }) => {
  const page = await pageQuery(url, fetch);

  return { page };
};
