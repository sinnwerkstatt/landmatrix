<script lang="ts">
  import ImageBlock from "$components/Wagtail/ImageBlock.svelte";

  export let value;
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

<div class="siema w-full mx-auto max-w-[600px] max-h-[800px]">
  {#each value.images as image}
    <ImageBlock value={image} />
  {/each}
</div>
