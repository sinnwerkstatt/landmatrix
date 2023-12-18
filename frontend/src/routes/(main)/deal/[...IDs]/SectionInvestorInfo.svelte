<script lang="ts">
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import type { DealVersion2, InvestorHull } from "$lib/types/newtypes"

  import TextField from "$components/Fields/Display2/TextField.svelte"

  import Subsection from "./Subsection.svelte"

  export let version: DealVersion2

  let investor: InvestorHull | null = null

  async function fetchInvestor() {
    if (!version.operating_company) return
    console.log(version.operating_company)

    const ret = await fetch(`/api/investors/${version.operating_company.investor}/`)
    investor = await ret.json()
    console.log(investor)
  }
  onMount(() => {
    fetchInvestor()
  })

  //   const ret = await $page.data.urqlClient
  //     .query<{ investor: Investor }>(
  //       gql`
  //         query ($id: Int!) {
  //           investor(id: $id) {
  //             id
  //             name
  //             classification
  //             country {
  //               id
  //               name
  //             }
  //             homepage
  //             comment
  //             deals {
  //               id
  //               country {
  //                 id
  //                 name
  //               }
  //               intention_of_investment
  //               implementation_status
  //               negotiation_status
  //               intended_size
  //               contract_size
  //             }
  //           }
  //         }
  //       `,
  //       { id: deal?.operating_company?.id },
  //     )
</script>

<section>
  <Subsection
    title={$_("Operating Company")}
    fields={[
      version.operating_company,
      version.involved_actors,
      version.project_name,
      version.investment_chain_comment,
    ]}
  >
    <TextField
      fieldname="operating_company"
      label={$_("Operating Company")}
      value={version.operating_company.name}
    />
    <TextField
      fieldname="involved_actors"
      label={$_("Comment on investment chain ")}
      value={version.involved_actors}
    />
    <TextField
      fieldname="project_name"
      label={$_("Comment on investment chain ")}
      value={version.project_name}
    />
    <TextField
      fieldname="investment_chain_comment"
      label={$_("Comment on investment chain ")}
      value={version.investment_chain_comment}
    />
  </Subsection>
</section>
