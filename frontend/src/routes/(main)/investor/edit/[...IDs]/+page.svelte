<script lang="ts">
  import InvestorEditForm from "$components/Investor/InvestorEditForm.svelte"

  export let data
</script>

<InvestorEditForm
  investor={data.investor}
  investorID={data.investorID}
  investorVersion={data.investorVersion}
/>
