<script lang="ts">
  import { slide } from "svelte/transition"

  import { browser } from "$app/environment"

  interface FAQ {
    slug: string
    question: string
    answer: string
  }

  interface Props {
    value: { faqs: FAQ[] }
  }

  let { value }: Props = $props()

  let locationHash = $state(browser ? location.hash : undefined)

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
        type="button"
        class="btn-outline w-full whitespace-normal py-4 text-left tracking-wide"
        id="faq-{index}-question"
        onclick={() => updateHash(`#${faq.slug}`)}
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

<style lang="postcss">
  :global([data-block="faqs_block"] ul) {
    @apply list-disc pb-4 pl-6;
  }
  :global([data-block="faqs_block"] ol) {
    @apply list-decimal pb-4 pl-6;
  }
</style>
