<script lang="ts">
  // export let value
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
  }
</script>

<div
  class="bg-orange px-12 py-[80px] lg:grid lg:grid-cols-2 lg:gap-[120px] lg:px-[80px] xl:px-[120px]"
>
  <div>
    <h2 class="caption">{value.title}</h2>
    <h3 class="heading3 xl:heading1">{value.subtitle}</h3>
    <p class="body1 pb-[32px]">{@html value.text}</p>
    <a
      href={value.link.href}
      rel={value.link.rel_external ? "external" : ""}
      target={value.link.rel_external ? "_blank" : ""}
    >
      <div class="button1 w-fit rounded bg-black py-[10px] px-[20px] text-white">
        {value.link.text}
      </div>
    </a>
  </div>
  <div class="mx-auto my-auto">
    <img src={value.image.url} loading="lazy" />
  </div>
</div>
