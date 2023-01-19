<script lang="ts">
  import ImageBlock from "$components/Wagtail/ImageBlock.svelte"

  export let value
  // export default Vue.extend({
  //   props: {
  //     value: { type: Object, required: true },
  //   },
  //   mounted() {
  //     new Siema({
  //       selector: ".siema",
  //       duration: 200,
  //       easing: "ease-out",
  //       perPage: 1,
  //       // startIndex: 0,
  //       draggable: true,
  //       loop: false,
  //     });
  //     console.log("aho");
  //   },
  // });
</script>

<div data-block="slider" class="siema mx-auto max-h-[800px] w-full max-w-[600px]">
  {#each value.images as image}
    <ImageBlock value={image} />
  {/each}
</div>
