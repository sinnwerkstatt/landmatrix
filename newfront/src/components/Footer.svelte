<script lang="ts">
  import TwitterIcon from "$components/icons/TwitterIcon.svelte";
  import FacebookIcon from "$components/icons/FacebookIcon.svelte";
  import { _ } from "svelte-i18n";
</script>

<footer class="px-4 py-1.5 relative bg-lm-dark text-sm text-white">
  <div class="text-center">
    <p class="mb-0">
      &copy; {new Date().getFullYear()} The Land Matrix |
      {$_("All rights reserved")}
    </p>
  </div>
  <div class="absolute right-4 top-[5px]">
    <a
      class="hover:text-orange-light"
      target="_blank"
      href="https://twitter.com/Land_Matrix"
    >
      <TwitterIcon />
    </a>
    <a
      class="ml-2 hover:text-orange-light"
      target="_blank"
      href="https://www.facebook.com/LandMatrix"
    >
      <FacebookIcon />
    </a>
  </div>
</footer>
