<script context="module" lang="ts">
  import { i18nload } from "$lib/i18n/i18n";
  import type { Load } from "@sveltejs/kit";
  import { fetchBasis } from "$lib/stores";
  import Cookies from "js-cookie";

  export const load: Load = async ({ params }) => {
    const lang = Cookies.get("django_language") ?? "en";
    await fetchBasis(lang);
    await i18nload(params);
    return {};
  };
</script>

<script>
  import "../app.css";
  import Footer from "$components/Footer.svelte";
  import Navbar from "$components/Navbar.svelte";
  import NavigationLoader from "$components/NavigationLoader.svelte";
</script>

<NavigationLoader />
<Navbar />
<div class="h-[calc(100vh-58px-32px)] overflow-x-auto pb-12 px-2">
  <slot />
</div>
<Footer />
