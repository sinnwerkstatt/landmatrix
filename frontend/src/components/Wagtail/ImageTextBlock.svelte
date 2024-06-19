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
      title: string
    }
    bg_color: "white" | "orange"
  }
  $: isBgOrange = value.bg_color === "orange"
</script>

<div class="h-full py-24" class:bg-orange={isBgOrange}>
  <div class="container mx-auto px-10 lg:grid lg:grid-cols-2 lg:gap-[120px]">
    <div
      class="flex flex-col justify-center text-center text-gray-900 lg:text-left"
      class:dark:text-white={!isBgOrange}
    >
      <h2 class="caption">{value.title}</h2>
      <h3 class="heading2 xl:heading1">
        {value.subtitle}
      </h3>
      <p class="body1 lg:pb-8">{@html value.text}</p>
      <a
        class="btn btn-black hidden w-fit lg:block"
        href={value.link.href}
        rel={value.link.rel_external ? "external" : ""}
        target={value.link.rel_external ? "_blank" : ""}
      >
        {value.link.text}
      </a>
    </div>
    <div class="mx-auto my-auto flex justify-center">
      <img alt={value.image.title} src={value.image.url} loading="lazy" />
    </div>
    <a
      class="btn btn-black mx-auto mt-5 block w-fit lg:hidden"
      href={value.link.href}
      rel={value.link.rel_external ? "external" : ""}
      target={value.link.rel_external ? "_blank" : ""}
    >
      {value.link.text}
    </a>
  </div>
</div>
