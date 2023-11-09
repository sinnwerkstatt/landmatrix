{#if $$slots?.default}
  <div class="container isolate mx-auto mb-6 mt-8 lg:mb-12 lg:mt-16">
    <h1 class="heading2 mx-auto w-fit px-4">
      <span class="relative z-10 bg-white text-orange dark:bg-lm-black {$$props.class}">
        <slot />
      </span>
    </h1>
  </div>
{/if}
