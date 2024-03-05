<script lang="ts">
  import type { BlogPage } from "$lib/types/wagtail"

  import NewArticleList from "$components/Wagtail/NewArticleList.svelte"

  export let value: {
    title: string
    subtitle: string
    image: string
    articles: BlogPage[]
  }
</script>

<div data-block="new_resources_teasers" class="container mx-auto my-20 px-10 py-6 pb-0">
  <h2 class="caption text-center lg:text-left dark:text-white">{value.title}</h2>
  <h3 class="heading2 xl:heading1 text-center lg:text-left dark:text-white">
    {value.subtitle}
  </h3>
  <div class="lg:grid lg:grid-cols-10">
    <div class="mb-12 lg:col-span-5">
      <img
        class="min-h-[500px] bg-gray-50"
        src={value.image}
        alt="Featured resource thumbnail"
      />
      <div class="my-[24px]">
        <p class="caption text-orange">{value.articles[0].categories[0]?.name}</p>
        <h4 class="heading4 -mt-3 text-orange">{value.articles[0].title}</h4>

        <div class="body2 -mt-3 mb-6">{value.articles[0].date}</div>
        <p class="body1">
          {@html value.articles[0].excerpt}
        </p>
        <a class="button1 text-pelorous" href={value.articles[0].url}>Read more >></a>
      </div>
    </div>
    <div class="lg:col-span-4 lg:col-start-7">
      <NewArticleList articles={value.articles.slice(1)} />
    </div>
  </div>
</div>
