import type { GetSession, Handle } from "@sveltejs/kit";

export const handle: Handle = async ({ event, resolve }) => {
  event.locals.cookie = event.request.headers.get("cookie") ?? undefined;
  return resolve(event, {});
};

export const getSession: GetSession = (event) => {
  let languages;

  try {
    languages = event.request.headers
      ?.get("accept-language")
      ?.split(",")
      ?.map((l) => {
        return l.split(";")[0];
      }) ?? ["en"];
  } catch {
    languages = ["en"];
  }
  return { languages, cookie: event.locals.cookie };
};

// export const externalFetch: ExternalFetch = async request => {
//   console.log("EXTERNAL FETCH", request.url);
//   return fetch(request);
// };
