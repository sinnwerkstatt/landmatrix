<script lang="ts">
  import { _ } from "svelte-i18n"

  import FacebookIcon from "$components/icons/FacebookIcon.svelte"
  import TwitterIcon from "$components/icons/TwitterIcon.svelte"
</script>

<footer class="sticky bg-lm-dark px-2 py-1.5 text-sm text-white">
  <div class="text-left md:text-center">
    <p class="mb-0 w-5/6 truncate md:w-full">
      &copy; {new Date().getFullYear()} The Land Matrix |
      {$_("All rights reserved")}
    </p>
  </div>
  <div class="absolute right-4 top-[5px]">
    <a
      class="hover:text-orange-light"
      target="_blank"
      rel="noreferrer"
      href="https://twitter.com/Land_Matrix"
    >
      <TwitterIcon />
    </a>
    <a
      class="hover:text-orange-light ml-2"
      target="_blank"
      rel="noreferrer"
      href="https://www.facebook.com/LandMatrix"
    >
      <FacebookIcon />
    </a>
  </div>
</footer>
