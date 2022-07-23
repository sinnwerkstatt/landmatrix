<script lang="ts">
  import { onMount } from "svelte";
  import { _ } from "svelte-i18n";
  import type { Deal } from "$lib/types/deal";
  import type { Investor } from "$lib/types/investor";
  import { sortFn } from "$lib/utils";

  export let objects: Array<Deal | Investor>;

  export let sortBy;
  const sortLogic = () => {
    const allTHs = document.querySelectorAll("th");
    allTHs.forEach((th) => {
      th.addEventListener("click", () => {
        allTHs.forEach((th) => {
          th.classList.remove("asc", "desc");
        });

        if (sortBy === th.dataset.sortby) {
          sortBy = `-${th.dataset.sortby}`;
          th.classList.add("asc");
        } else {
          sortBy = th.dataset.sortby;
          th.classList.add("desc");
        }
      });
    });
  };

  let _objects;

  $: _objects = objects ? (sortBy ? [...objects].sort(sortFn(sortBy)) : objects) : [];

  onMount(() => {
    sortLogic();

    // if sortBy is set on mount, apply it as well.
    if (sortBy) {
      if (sortBy.startsWith("-")) {
        document
          .querySelector(`th[data-sortby="${sortBy.substring(1)}"]`)
          ?.classList?.add("asc");
      } else {
        document.querySelector(`th[data-sortby="${sortBy}"]`)?.classList?.add("desc");
      }
    }
  });
</script>

<div class="overflow-auto h-full pb-20">
  <table class="table-auto w-full border-b-2 relative">
    <slot name="thead" />

    {#if _objects.length > 0}
      <slot name="tbody" objects={_objects} />
    {:else}
      <tbody>
        <tr>
          <td colspan="42" class="text-center text-gray-500">{$_("No entries")}</td>
        </tr>
      </tbody>
    {/if}
  </table>
</div>

<style>
  :global(th[data-sortby]) {
    @apply pr-5;
  }
  :global(th[data-sortby]::after) {
    content: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 20 20" fill="gray"><path d="m 14.707,8.707 a 1,1 0 0 1 -1.414,0 L 10,5.414 6.707,8.707 A 1,1 0 0 1 5.293,7.293 l 4,-4 a 1,1 0 0 1 1.414,0 l 4,4 a 1,1 0 0 1 0,1.414 z" /> <path     d="m 5.293,11.293 a 1,1 0 0 1 1.414,0 L 10,14.586 13.293,11.293 a 1,1 0 1 1 1.414,1.414 l -4,4 a 1,1 0 0 1 -1.414,0 l -4,-4 a 1,1 0 0 1 0,-1.414 z" /></svg>');
    position: absolute;
    top: 25%;
  }

  :global(th[data-sortby].asc::after) {
    /*content: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 20 20" fill="%230c5e9c"> <path d="m 14.707,8.707 a 1,1 0 0 1 -1.414,0 L 10,5.414 6.707,8.707 A 1,1 0 0 1 5.293,7.293 l 4,-4 a 1,1 0 0 1 1.414,0 l 4,4 a 1,1 0 0 1 0,1.414 z" /></svg>');*/
    content: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 20 20" fill="%23fc941f"> <path d="m 14.707,8.707 a 1,1 0 0 1 -1.414,0 L 10,5.414 6.707,8.707 A 1,1 0 0 1 5.293,7.293 l 4,-4 a 1,1 0 0 1 1.414,0 l 4,4 a 1,1 0 0 1 0,1.414 z" /></svg>');
  }

  :global(th[data-sortby].desc::after) {
    content: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 20 20" fill="%23fc941f"><path d="m 5.293,11.293 a 1,1 0 0 1 1.414,0 L 10,14.586 13.293,11.293 a 1,1 0 1 1 1.414,1.414 l -4,4 a 1,1 0 0 1 -1.414,0 l -4,-4 a 1,1 0 0 1 0,-1.414 z" /></svg>');
  }
</style>
