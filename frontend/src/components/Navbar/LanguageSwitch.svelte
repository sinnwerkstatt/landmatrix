<script lang="ts">
  import Cookies from "js-cookie"
  import { locale } from "svelte-i18n"

  import LanguageIcon from "$components/icons/LanguageIcon.svelte"
  import NavDropDown from "$components/Navbar/NavDropDown.svelte"

  const languages: { [key: string]: string } = {
    en: "English",
    es: "Español",
    fr: "Français",
    ru: "Русский",
  }

  const switchLanguage = async (lang: string) => {
    Cookies.set("django_language", lang)
    await locale.set(lang)
  }
</script>

<NavDropDown>
  <svelte:fragment slot="title">
    <span class="button1 mx-3 text-black dark:text-white">
      <span class="hidden md:inline">{languages[$locale ?? "en"]}</span>
      <span class="md:hidden"><LanguageIcon /></span>
    </span>
  </svelte:fragment>

  <ul class="bg-white shadow-lg dark:bg-gray-900">
    {#each Object.entries(languages) as [lcode, lingo]}
      <li>
        <button
          class="nav-link w-full whitespace-nowrap px-6"
          class:active={lcode === $locale}
          on:click={() => switchLanguage(lcode)}
        >
          <span class="capitalize">{lingo}</span>
          <span class="lowercase">({lcode})</span>
        </button>
      </li>
    {/each}
  </ul>
</NavDropDown>
