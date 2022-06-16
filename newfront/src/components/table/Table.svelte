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

<div class="overflow-auto h-full">
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
