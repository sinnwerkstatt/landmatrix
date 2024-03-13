<script lang="ts">
  import { slide } from "svelte/transition"

  import { browser } from "$app/environment"

  interface FAQ {
    slug: string
    question: string
    answer: string
  }

  export let value: { faqs: FAQ[] }

  let locationHash = browser ? location.hash : undefined

  const updateHash = (slug: string) => {
    if (!browser) return
    location.hash = location.hash === slug ? "" : slug
    locationHash = location.hash
  }
</script>

<div data-block="faqs_block" class="flex flex-col gap-2">
  {#each value.faqs as faq, index}
    <article id="faq-{index}-{faq.slug}">
      <button
        class="btn w-full whitespace-normal py-4 text-left tracking-wide
          dark:border-orange dark:bg-gray-900 dark:text-white"
        id="faq-{index}-question"
        on:click={() => updateHash(`#${faq.slug}`)}
      >
        {faq.question}
      </button>
      {#if locationHash === `#${faq.slug}`}
        <div transition:slide id="faq-{index}-answer" class="p-4">
          {@html faq.answer}
        </div>
      {/if}
    </article>
  {/each}
</div>
