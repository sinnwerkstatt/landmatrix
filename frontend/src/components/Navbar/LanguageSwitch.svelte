<script lang="ts">
  import Cookies from "js-cookie"
  import { locale } from "svelte-i18n"

  import { fetchAboutPages, fetchObservatoryPages } from "$lib/stores/wagtail"

  import LanguageIcon from "$components/icons/LanguageIcon.svelte"
  import NavDropDown from "$components/Navbar/NavDropDown.svelte"

  const languages: { [key: string]: string } = {
    en: "English",
    es: "Español",
    fr: "Français",
    ru: "Русский",
  }

  const switchLanguage = async (lang: string) => {
    Cookies.set("django_language", lang, { sameSite: "lax" })
    await locale.set(lang)

    await fetchObservatoryPages(fetch, lang)
    await fetchAboutPages(fetch, lang)
  }
</script>

<NavDropDown>
  {#snippet title()}
    <span class="nav-link-main mx-2 inline-block">
      <span class="hidden md:inline">{languages[$locale ?? "en"]}</span>
      <span class="md:hidden"><LanguageIcon /></span>
    </span>
  {/snippet}

  <ul class="bg-white text-sm shadow-lg dark:bg-gray-900">
    {#each Object.entries(languages) as [lcode, lingo]}
      <li>
        <button
          type="button"
          class="nav-link-secondary"
          class:active={lcode === $locale}
          onclick={() => switchLanguage(lcode)}
        >
          <span class="capitalize">{lingo}</span>
          <span class="lowercase">({lcode})</span>
        </button>
      </li>
    {/each}
  </ul>
</NavDropDown>
