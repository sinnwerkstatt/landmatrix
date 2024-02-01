<script lang="ts">
  import Cookies from "js-cookie"
  import { locale } from "svelte-i18n"

  import { fetchBasis, fetchFieldDefinitions } from "$lib/stores"

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
    await fetchBasis(fetch)
  }
</script>

<NavDropDown>
  <svelte:fragment slot="title">
    <span class="button1 mx-3 text-black dark:text-white">
      {languages[$locale]}
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
          <span class="uppercase">({lcode})</span>
        </button>
      </li>
    {/each}
  </ul>
</NavDropDown>
