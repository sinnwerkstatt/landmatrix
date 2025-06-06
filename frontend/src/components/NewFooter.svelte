<script lang="ts">
  import type { Component } from "svelte"
  import { _ } from "svelte-i18n"

  import FacebookIcon from "$components/icons/FacebookIcon.svelte"
  import LinkedInIcon from "$components/icons/LinkedInIcon.svelte"
  import TwitterIcon from "$components/icons/TwitterIcon.svelte"
  import YoutubeIcon from "$components/icons/YoutubeIcon.svelte"
  import Newsletter from "$components/Newsletter.svelte"

  let menuEntries: {
    title: string
    href: string
  }[] = $derived([
    { title: $_("Data policy"), href: "/data-policy/" },
    { title: $_("Privacy policy"), href: "/privacy-policy/" },
    { title: $_("Impressum / Legal notice"), href: "/impressum-legal-notice/" },
    { title: $_("Disclaimer"), href: "/disclaimer/" },
  ])

  let socialEntries: {
    title: string
    href: string
    icon: Component
  }[] = $derived([
    {
      title: "Facebook",
      href: "https://www.facebook.com/LandMatrix",
      icon: FacebookIcon,
    },
    {
      title: "Twitter",
      href: "https://twitter.com/Land_Matrix",
      icon: TwitterIcon,
    },
    {
      title: "Youtube",
      href: "https://www.youtube.com/@landmatrixinitiativelmi6450",
      icon: YoutubeIcon,
    },
    {
      title: "LinkedIn",
      href: "https://www.linkedin.com/company/land-matrix-initiative/",
      icon: LinkedInIcon,
    },
  ])
</script>

<div class="bg-gray-700 pt-12 text-white">
  <div class="mb-5 px-10 sm:text-center lg:mb-12">
    <h4 class="heading5 mx-2">
      {$_(
        "Sign up for our eBulletins to receive important updates from the Land Matrix about key events and publications",
      )}
    </h4>
    <Newsletter />
  </div>
  <div class="container mx-auto p-10 pt-5 lg:p-4">
    <hr class="my-10 text-white lg:hidden" />

    <div class="flex flex-col gap-2 lg:flex-row lg:justify-center lg:gap-8">
      {#each menuEntries as entry}
        <a class="text-white hover:text-orange" href={entry.href}>
          {entry.title}
        </a>
      {/each}
    </div>

    <div class="mt-10 lg:mt-2 lg:flex lg:justify-center lg:gap-4">
      <span class="subtitle1 after:content-[':']">
        {$_("Follow us")}
      </span>
      <div class="mt-3 flex gap-3 lg:mt-0 lg:inline-flex lg:align-bottom">
        {#each socialEntries as entry}
          <a
            class="text-white hover:text-orange"
            target="_blank"
            rel="noreferrer noopener"
            title={entry.title}
            href={entry.href}
          >
            <entry.icon />
          </a>
        {/each}
      </div>
    </div>

    <div class="mt-10 lg:mt-3">
      <span>
        &copy; {new Date().getFullYear()} The Land Matrix |
        {$_("All rights reserved")}
      </span>
    </div>
  </div>
</div>
