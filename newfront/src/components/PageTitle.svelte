{#if $$slots?.default}
  <div class="container isolate mx-auto mt-9 mb-5">
    <h1
      class="relative text-center text-3xl before:absolute before:top-1/2 before:block before:h-[1px] before:w-full before:bg-gray-300 before:content-[''] dark:before:bg-gray-500"
    >
      <span
        class="relative z-10 bg-white px-4 font-bold uppercase uppercase text-orange dark:bg-gray-800 {$$props.class}"
      >
        <slot />
      </span>
    </h1>
  </div>
{/if}
