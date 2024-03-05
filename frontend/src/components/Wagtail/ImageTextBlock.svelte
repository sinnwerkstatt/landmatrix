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

<div class="py-10" class:bg-orange={value.bg_color === "orange"}>
  <div class="container mx-auto px-10 lg:grid lg:grid-cols-2 lg:gap-[120px]">
    <div class="flex flex-col justify-center text-center lg:text-left">
      <h2 class="caption text-gray-900">{value.title}</h2>
      <h3 class="heading2 xl:heading1 text-gray-900">{value.subtitle}</h3>
      <p class="body1 lg:pb-8 dark:text-gray-900">{@html value.text}</p>
      <a
        class="button1 hidden w-fit rounded bg-black px-5 py-[10px] text-white transition hover:bg-opacity-80 lg:block"
        href={value.link.href}
        rel={value.link.rel_external ? "external" : ""}
        target={value.link.rel_external ? "_blank" : ""}
      >
        {value.link.text}
      </a>
    </div>
    <div class="mx-auto my-auto flex justify-center">
      <img src={value.image.url} loading="lazy" />
    </div>
    <a
      class="button1 mx-auto block w-fit rounded bg-black px-5 py-[10px] text-white transition hover:bg-gray-700 lg:hidden"
      href={value.link.href}
      rel={value.link.rel_external ? "external" : ""}
      target={value.link.rel_external ? "_blank" : ""}
    >
      {value.link.text}
    </a>
  </div>
</div>
