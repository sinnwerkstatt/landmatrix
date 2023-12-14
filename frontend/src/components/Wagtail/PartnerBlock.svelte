<script lang="ts">
  import PartnerSlider from "$components/PartnerSlider.svelte"

  export let value

  let donors = value.filter(p => p.category === "Donors")
  let partners = value.filter(p => p.category === "Partners")
</script>

<div class="mx-auto bg-white py-20 py-6 text-center">
  {#if donors}
    <h2 class="heading3 text-lm-black">Donors</h2>
    <PartnerSlider partners={donors} countSlides={3} />
  {/if}
  {#if partners}
    <h2 class="heading3 text-lm-black">Partners</h2>
    <PartnerSlider {partners} countSlides={4} />
  {/if}
</div>
