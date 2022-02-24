<script context="module" lang="ts">
  import { i18nload } from "$lib/i18n/i18n";
  import type { LoadInput, LoadOutput } from "@sveltejs/kit";
  import { getAboutPages, getBlogCategories, getObservatoryPages } from "$lib/stores";

  export async function load({ params }: LoadInput): Promise<LoadOutput> {
    await getObservatoryPages();
    await getBlogCategories();
    await getAboutPages();

    await i18nload(params);
    return {};
  }
</script>
<script>
	import '../app.css';
	import Navbar from '../components/Navbar.svelte';
</script>

<Navbar />
<slot />
