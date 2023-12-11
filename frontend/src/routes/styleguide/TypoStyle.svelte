<script lang="ts">
  export let val: {
    title: string
    desktop: string
    mobile: string
    specs: { name: string; value: string; tw: string | undefined }[]
  }
</script>

<div class="my-12 grid grid-cols-2">
  <div class="flex flex-col">
    <h4 class={val.desktop}>{val.title}</h4>
    <h4 class={val.mobile}>{val.title}</h4>
  </div>
  <div class="grid grid-cols-2">
    {#each val.specs as x}
      <div>
        <div class="grid grid-cols-2">
          <div class="italic text-gray-dark">{x.name}</div>
          <div class="flex gap-3">
            {#if Array.isArray(x.value)}
              <div class="font-bold">{x.value[0]}</div>
              <div class="font-bold">{x.value[1]}</div>
            {:else}
              {x.value}
            {/if}
          </div>
        </div>
        {#if x.tw}
          <code class="code">{x.tw}</code>
        {/if}
      </div>
    {/each}
  </div>
</div>
