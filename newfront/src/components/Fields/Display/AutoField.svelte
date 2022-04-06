<script lang="ts">
  import type { FormField } from "$components/Fields/fields";

  export let formfield: FormField;
  export let value: number;
  export let model: string;
  export let targetBlank: boolean; //default false
  export let objectVersion: number; //required false

  // export default Vue.extend({
  //   props: {
  //     formfield: { type: Object as PropType<FormField>, required: true },
  //     value: { type: Number, required: true },
  //     model: { type: String, required: true },
  //     targetBlank: { type: Boolean, default: false },
  //     objectVersion: { type: Number, default: null, required: false },
  //   },
  // });
</script>

<div class="auto_field">
  {#if model === "deal"}
    <a
      class="id-display deal-id-display"
      target={() => {
        $targetBlank ? "_blank" : "_self";
      }}
    >
      <!--      :to="{-->
      <!--        name: 'deal_detail',-->
      <!--        params: { dealId: value, dealVersion: objectVersion },-->
      <!--      }"-->

      {value}
    </a>
  {:else if model === "investor"}
    <a
      class="id-display investor-id-display"
      target={() => {
        $targetBlank ? "_blank" : "_self";
      }}
    >
      <!--      :to="{-->
      <!--        name: 'investor_detail',-->
      <!--        params: { investorId: value, investorVersion: objectVersion },-->
      <!--      }"-->

      {value}</a
    >
  {:else}{value}
  {/if}
</div>
