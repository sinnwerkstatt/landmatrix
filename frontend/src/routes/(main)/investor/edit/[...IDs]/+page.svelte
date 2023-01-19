<script lang="ts">
  import InvestorEditForm from "$components/Investor/InvestorEditForm.svelte"

  import type { PageData } from "./$types"

  export let data: PageData
</script>

<InvestorEditForm
  investor={data.investor}
  investorID={data.investorID}
  investorVersion={data.investorVersion}
/>
