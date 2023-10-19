<script lang="ts">
  import { _ } from "svelte-i18n"

  export let value: {
    sum_ha: number
    deals: number
    text: string
  }
</script>

<div
  class="content-fit container mx-auto my-20 bg-[url('/images/Background_hoehenlinien.png')] bg-contain  p-6 text-center dark:bg-[url('/images/Background_hoehenlinien_dark.png')]"
>
  <h3 class="heading1 dark:text-white">{value.text}</h3>
  <p class="display1 text-pelorous">{value.deals} {$_("deals")}</p>
  <p class="heading2 text-pelorous-300">
    {$_("Equals")}
    {value.sum_ha.toLocaleString("fr") ?? "—"}
    {$_("ha")}
  </p>
</div>
