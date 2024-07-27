import { init, register, waitLocale } from "svelte-i18n"

export const SUPPORTED_LANGUAGES = ["en", "es", "fr", "ru"] as const
export type Lang = typeof SUPPORTED_LANGUAGES[number]

export async function i18nload(lang: Lang): Promise<void> {
  SUPPORTED_LANGUAGES.forEach(locale => {
    register(locale, () => import(`./lang_${locale}.json`))
  })

  await init({
    fallbackLocale: "en",
    initialLocale: lang,
    warnOnMissingMessages: false,
  })
  await waitLocale()
}
