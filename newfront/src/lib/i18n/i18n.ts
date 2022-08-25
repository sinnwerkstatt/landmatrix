import { init, register, waitLocale } from "svelte-i18n";

export const supportedLanguages = ["en", "es", "fr", "ru"];
export async function i18nload(lang: string): Promise<void> {
  // these "params" are taken from [lang] in the routes-folder
  // const { lang } = params;

  supportedLanguages.forEach((locale) => {
    register(locale, () => import(`./lang_${locale}.json`));
  });

  await init({
    fallbackLocale: "en",
    initialLocale: lang,
    warnOnMissingMessages: false,
  });
  await waitLocale();
}

// import { browser } from "$app/env";
// export function detectLang(languages: string[]): string {
//   if (!languages)
//     languages = browser
//       ? [window.navigator.language, ...window.navigator.languages]
//       : ["en"];
//   for (const browserLocale of languages) {
//     for (const supportedLanguage of supportedLanguages) {
//       if (browserLocale.startsWith(supportedLanguage)) return supportedLanguage;
//     }
//   }
//   return "en";
// }
