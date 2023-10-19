<script lang="ts">
  import { locale } from "svelte-i18n"
  import Cookies from "js-cookie"

  import { page } from "$app/stores"

  import { fetchBasis, fetchFieldDefinitions } from "$lib/stores"

  import TranslateIcon from "$components/icons/TranslateIcon.svelte"
  import NavDropDown from "$components/Navbar/NavDropDown.svelte"

  const languages = {
    en: "English",
    es: "Español",
    fr: "Français",
    ru: "Русский",
  }

  const switchLanguage = async (lang: string) => {
    Cookies.set("django_language", lang)
    await locale.set(lang)
    await fetchFieldDefinitions(fetch)
    await fetchBasis(lang, fetch, $page.data.urqlClient)
  }
</script>

<NavDropDown>
  <svelte:fragment slot="title">
    <span class="button1 mx-3 text-black underline">{languages[$locale]}</span>
  </svelte:fragment>

  <ul class="border-2 border-orange bg-white dark:bg-gray-800">
    {#each Object.entries(languages) as [lcode, lingo]}
      <li>
        <button
          class="nav-link w-full whitespace-nowrap"
          class:active={lcode === $locale}
          on:click={() => switchLanguage(lcode)}
        >
          <span class="capitalize">{lingo}</span>
          <span class="uppercase">({lcode})</span>
        </button>
      </li>
    {/each}
  </ul>
</NavDropDown>
