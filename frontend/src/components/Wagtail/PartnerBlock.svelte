<script lang="ts">
  export let value

  let donors = value.filter(p => p.category === "Donors")
  let partners = value.filter(p => p.category === "Partners")
</script>

<div class="mx-auto bg-white py-20 py-6 text-center">
  <h2 class="heading3 text-lm-black">Donors</h2>
  <div class="mb-12 flex flex-wrap justify-center">
    {#each donors as donor}
      <div class=" p-6">
        <a href={donor.homepage} target="_blank">
          <img src={donor.logo} alt={donor.name} />
        </a>
      </div>
    {/each}
  </div>
  <h2 class="heading3 text-lm-black">Partners</h2>
  <div class="flex flex-wrap justify-center">
    {#each partners as partner}
      <div class="flex items-center px-6">
        <a href={partner.homepage} target="_blank">
          <img src={partner.logo} alt={partners.name} />
        </a>
      </div>
    {/each}
  </div>
</div>
