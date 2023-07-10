<script lang="ts">
  let value = ""

  let actives = []
  let drafts = []
  async function getSearchResults(v) {
    if (value.length < 3) {
      actives = []
      drafts = []
      return
    }
    let ret = await fetch(`/api/investor_search/?q=${v}`)
    const retJson = await ret.json()
    actives = retJson.investors.filter(i => i.status !== 1)
    drafts = retJson.investors.filter(i => i.status === 1)
  }
  $: getSearchResults(value)
</script>

<div class="mt-12 flex w-full items-center justify-center">
  <h1>Investor search</h1>
</div>

<div class="container mx-auto">
  <form class="flex justify-center">
    <input bind:value class="inpt w-1/2" placeholder="" />
  </form>

  <div class="mt-10">
    <ul>
      {#each actives as investor}
        <li class="py-0.5 odd:bg-gray-100">
          <a class="investor flex" href="/investor/{investor.id}/" target="_blank">
            <span class="w-[5rem]">[{investor.id}]</span>
            <span class="min-w-[10rem] px-4">{investor.country__name}</span>
            {investor.name}
          </a>
        </li>
      {/each}
    </ul>
    {#if drafts.length}
      Drafts:

      <ul>
        {#each drafts as investor}
          <li class="py-0.5 odd:bg-gray-100">
            <a class="investor flex" href="/investor/{investor.id}/" target="_blank">
              <span class="w-[5rem]">[{investor.id}]</span>
              <span class="min-w-[10rem] px-4">{investor.country__name}</span>
              {investor.name}
            </a>
          </li>
        {/each}
      </ul>
    {/if}
  </div>
</div>
