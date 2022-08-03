{#if $$slots?.default}
  <div class="container mx-auto mt-9 mb-5 isolate">
    <h1
      class="text-center relative text-3xl before:content-[''] before:bg-gray-300 dark:before:bg-gray-500 before:block before:h-[1px] before:absolute before:top-1/2 before:w-full"
    >
      <span
        class="uppercase font-bold text-orange uppercase px-4 relative bg-white dark:bg-gray-800 z-10 {$$props.class}"
      >
        <slot />
      </span>
    </h1>
  </div>
{/if}
