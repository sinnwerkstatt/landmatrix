<script lang="ts">
  export let value: {
    title: string
    subtitle: string
    text: string
    link: {
      href: string
      rel_external: boolean
      text: string
    }
    image: {
      id: number
      url: string
    }
    bg_color: string
  }
</script>

<div
  class="mb-20 min-h-[calc(100vh-71px)]"
  class:bg-orange={value.bg_color === "orange"}
>
  <div class="container mx-auto px-10 py-20 lg:grid lg:grid-cols-2 lg:gap-[120px]">
    <div class="flex flex-col justify-center text-center lg:text-left">
      <h2 class="caption text-gray-900">{value.title}</h2>
      <h3 class="heading3 xl:heading1 text-gray-900">{value.subtitle}</h3>
      <p class="body1 lg:pb-8 dark:text-gray-900">{@html value.text}</p>
      <a
        class="hidden lg:block"
        href={value.link.href}
        rel={value.link.rel_external ? "external" : ""}
        target={value.link.rel_external ? "_blank" : ""}
      >
        <div
          class="button1 w-fit rounded bg-black px-5 py-[10px] text-white transition hover:bg-opacity-80"
        >
          {value.link.text}
        </div>
      </a>
    </div>
    <div class="mx-auto my-auto flex justify-center">
      <img src={value.image.url} loading="lazy" />
    </div>
    <a
      class="block lg:hidden"
      href={value.link.href}
      rel={value.link.rel_external ? "external" : ""}
      target={value.link.rel_external ? "_blank" : ""}
    >
      <div
        class="button1 mx-auto w-fit rounded bg-black px-5 py-[10px] text-white transition hover:bg-gray-700"
      >
        {value.link.text}
      </div>
    </a>
  </div>
</div>
