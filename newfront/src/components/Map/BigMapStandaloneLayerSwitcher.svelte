<script>
  import LayerGroup from "$components/icons/LayerGroup.svelte";
  import { visibleLayer, baseLayers } from "./layers";

  let shown;
</script>

<div
  class="absolute top-[10px] right-[10px] z-10 rounded border-2 border-black/30 bg-white px-2 pt-1 pb-2"
  on:mouseleave={() => (shown = false)}
>
  {#if !shown}
    <LayerGroup
      class="inline h-5 w-5 text-orange"
      on:focus={() => (shown = true)}
      on:mouseover={() => (shown = true)}
    />
  {:else}
    <ul>
      {#each baseLayers as layer}
        <li class="p-1">
          {#if layer.name === $visibleLayer}
            <div>{layer.name}</div>
          {:else}
            <button
              on:click|preventDefault={() => visibleLayer.set(layer.name)}
              class="text-orange"
            >
              {layer.name}
            </button>
          {/if}
        </li>
      {/each}
    </ul>
  {/if}
</div>
