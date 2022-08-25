import { init, register, waitLocale } from "svelte-i18n";

export const supportedLanguages = ["en", "es", "fr", "ru"];
export async function i18nload(lang: string): Promise<void> {
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
