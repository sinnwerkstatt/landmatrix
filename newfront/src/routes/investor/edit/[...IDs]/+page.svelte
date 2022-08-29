<script lang="ts">
  import type { Investor } from "$lib/types/investor"

  import InvestorEditForm from "$views/InvestorEditForm.svelte"

  // import type { PageData } from "./$types";
  //
  // export let data: PageData;
  export let data: { investor: Investor; investorID: number; investorVersion: number }
</script>

<InvestorEditForm
  investor={data.investor}
  investorID={data.investorID}
  investorVersion={data.investorVersion}
/>
