<script lang="ts">
  import { _ } from "svelte-i18n";
  import ChevronUpIcon from "$components/icons/ChevronUpIcon.svelte";
  import ClearFilter from "$components/icons/ClearFilter.svelte";

  export let title: string;
  export let clearable = false;
  export let initExpanded = false;
  function toggle() {
    initExpanded = !initExpanded;
  }

  //$: paddingCollapse = ;

  function accordion(node) {
    let initialHeight = node.offsetHeight + 16;
    node.style.height = initExpanded ? "auto" : 0;
    node.style.overflow = "hidden";
    return {
      update(isOpen) {
        let animation = node.animate(
          [
            {
              height: initialHeight + "px",
              overflow: "hidden",
            },
            {
              height: 0,

              overflow: "hidden",
            },
          ],
          { duration: 300, fill: "both" }
        );
        animation.pause();
        if (!isOpen) {
          animation.play();
        } else {
          animation.reverse();
        }
      },
    };
  }
</script>

<div
  class="-mx-2 pl-1 border-b border-gray-300 bg-lm-lightgray text-lm-dark hover:cursor-pointer"
>
  <div
    class="py-1.5 pr-2 relative flex justify-between"
    class:text-orange={clearable}
    class:collapsed={!initExpanded}
    data-toggle="collapse"
  >
    <span class="pr-0" on:click={toggle}>
      <ChevronUpIcon
        class="{initExpanded
          ? 'rotate-180'
          : ''} transition transition-duration-300 mr-1 h-3 w-3 inline rounded"
      />
      {$_(title)}
    </span>
    {#if clearable}
      <ClearFilter on:click />
    {/if}
  </div>
  <div
    use:accordion={initExpanded}
    class={`shadow-inner bg-lm-light -ml-[0.5em] pl-2 ${initExpanded ? "py-2" : ""}`}
    class:show={initExpanded}
  >
    <slot />
  </div>
</div>

<style>
  /*<!--  .filter-collapse .toggle .expand-toggle {-->*/
  /*<!--    color: rgba(0, 0, 0, 0.3);-->*/
  /*<!--    font-weight: bold;-->*/
  /*<!--    font-size: 12px;-->*/
  /*<!--    margin-right: 3px;-->*/
  /*<!--    transition: all 0.1s ease;-->*/
  /*<!--  }-->*/

  /*ul {*/
  /*  padding-left: 0.3em;*/
  /*  list-style: none;*/
  /*}*/

  /*.expand-slot {*/
  /*box-shadow: inset 0 3px 7px -3px rgba(0, 0, 0, 0.1),*/
  /*  inset 0 -2px 5px -2px rgba(0, 0, 0, 0.1);*/
  /*background-color: rgba(0, 0, 0, 0.01);*/
  /*padding: 0.5em 0.5em;*/
  /*margin: 0 -0.5em;*/
  /*transition: all 0.1s ease;*/
  /*font-size: 14px;*/
  /*}*/
</style>
