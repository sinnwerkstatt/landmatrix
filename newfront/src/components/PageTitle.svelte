{#if $$slots?.default}
  <div class="container mx-auto mt-9 mb-5">
    <h1
      class="text-center relative text-3xl before:content-[''] before:bg-gray-300 before:block before:h-[1px] before:absolute before:top-1/2 before:w-full"
    >
      <span
        class="uppercase font-bold text-orange uppercase px-4 relative bg-white z-10"
      >
        <slot />
      </span>
    </h1>
  </div>
{/if}
