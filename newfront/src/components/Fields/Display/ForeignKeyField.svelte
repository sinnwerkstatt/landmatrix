<script lang="ts">
  import type { FormField } from "$components/Fields/fields";
  import type { Country } from "$lib/types/wagtail";
  import { countries } from "$lib/stores";

  export let formfield: FormField;
  export let value: object;
  export let model: string;

  $: calc_name = () => {
    if (!value || !value.id) return "";
    if (formfield.related_model === "Country" && $countries) {
      return $countries.find((c: Country) => c.id === this.value.id).name;
    }
    return value.username ?? value.name ?? value.id;
  };
</script>

<div class="foreignkey_field">
  {#if formfield.related_model === "Investor"}
    <a class="investor" target="_blank">
      <!--      to="{ name: 'investor_detail', params: { investorId: value.id } }"-->

      {value.name} (#{value.id})
    </a>
  {:else}{calc_name()}
  {/if}
</div>
