<script lang="ts">
  import { slide } from "svelte/transition"

  import { browser } from "$app/environment"

  export let value

  let locationHash = browser ? location.hash : undefined

  function updateHash(slug) {
    if (!browser) return
    let newslug
    if (location.hash === slug) newslug = ""
    else newslug = slug
    locationHash = newslug
    location.hash = newslug
  }
</script>

<div data-block="faqs_block" class="border border-gray-400">
  {#each value.faqs as faq}
    <div>
      <button
        class="w-full cursor-pointer border-b border-gray-400 bg-lm-dark py-4 px-6 text-left font-bold text-orange"
        on:click={() => updateHash(`#${faq.slug}`)}
      >
        {faq.question}
      </button>
      {#if locationHash === `#${faq.slug}`}
        <div
          transition:slide
          id="collapse-{faq.slug}"
          class="border-t border-gray-400 bg-white p-4 dark:bg-gray-600"
        >
          <div class="card-body">{@html faq.answer}</div>
        </div>
      {/if}
    </div>
  {/each}
</div>
