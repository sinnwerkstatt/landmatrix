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

<div class:bg-orange={value.bg_color === "orange"} class="mb-20">
  <div class="container mx-auto px-10 py-20 lg:grid lg:grid-cols-2 lg:gap-[120px]">
    <div class="flex flex-col justify-center text-center lg:text-left">
      <h2 class="caption text-lm-black">{value.title}</h2>
      <h3 class="heading3 xl:heading1 text-lm-black">{value.subtitle}</h3>
      <p class="body1 dark:text-lm-black lg:pb-8">{@html value.text}</p>
      <a
        class="hidden lg:block"
        href={value.link.href}
        rel={value.link.rel_external ? "external" : ""}
        target={value.link.rel_external ? "_blank" : ""}
      >
        <div
          class="button1 w-fit rounded bg-black py-[10px] px-5 text-white transition hover:scale-[105%]"
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
        class="button1 mx-auto w-fit rounded bg-black py-[10px] px-5 text-white transition hover:scale-[105%]"
      >
        {value.link.text}
      </div>
    </a>
  </div>
</div>
