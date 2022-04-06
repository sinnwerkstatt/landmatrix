<script lang="ts">
  import type { FormField } from "$components/Fields/fields";

  export let name = "ManyToManyField";
  export let formfield: FormField;
  export let value: object[];
  export let model: string;

  // export default Vue.extend({
  //   name: "ManyToManyField",
  //   props: {
  //     formfield: { type: Object as PropType<FormField>, required: true },
  //     value: { type: [Array, Object], required: true },
  //     model: { type: String, required: true },
  //   },
  // });
</script>

<div class="manytomany_field">
  {#if formfield.related_model === "Investor"}
    {#each value as val}
      <a class="investor" target="_blank" href="#">
        <!--          href="{ name: 'investor_detail', params: { investorId: val.id } }"-->

        {val.name} (#{val.id})
      </a>
      <br key="val.id" />
    {/each}
  {:else}
    {value}
  {/if}
</div>
