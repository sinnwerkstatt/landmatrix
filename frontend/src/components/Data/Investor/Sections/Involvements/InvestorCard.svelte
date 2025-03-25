<script lang="ts">
  import { _ } from "svelte-i18n"

  import { simpleInvestors } from "$lib/stores"
  import { InvolvementRole, type Involvement, type Model } from "$lib/types/data"

  import DisplayField from "$components/Fields/DisplayField.svelte"
  import SourcesDisplayButton from "$components/Quotations/SourcesDisplayButton.svelte"

  interface Props {
    involvement: Involvement
    isParent?: boolean
  }

  let { involvement, isParent = false }: Props = $props()

  const model: Model = "investor"

  const wrapperClass = "my-1 flex flex-wrap justify-between"
  const labelClass = "whitespace-nowrap font-light text-gray-400 pr-2 italic"
  const valueClass = "font-medium"

  let otherInvestorId: number = isParent
    ? involvement.parent_investor_id
    : involvement.child_investor_id

  let otherInvestor = $derived($simpleInvestors.find(i => i.id === otherInvestorId))

  let relationshipMap: { [key in InvolvementRole]: { parent: string; child: string } } =
    $derived({
      [InvolvementRole.PARENT]: {
        parent: $_("Parent company"),
        child: $_("Subsidiary company"),
      },
      [InvolvementRole.LENDER]: {
        parent: $_("Tertiary investor/lender"),
        child: $_("Beneficiary company"),
      },
    })

  let relationship = $derived(
    relationshipMap[involvement.role][isParent ? "parent" : "child"],
  )
</script>

{#if otherInvestor}
  {@const isDraft = !otherInvestor.active}
  {@const isDeleted = otherInvestor.deleted}
  {@const isDraftOrDeleted = isDraft || isDeleted}

  <div
    class="relative flex flex-col gap-1 border border-pelorous p-2"
    class:bg-yellow-100={isDraft}
    class:bg-red-200={isDeleted}
    class:bg-opacity-10={isDraftOrDeleted}
    class:pb-12={isDraftOrDeleted}
  >
    {#if isDraftOrDeleted}
      <div
        class="absolute bottom-2 left-0 right-0 text-center text-3xl italic"
        class:text-yellow-100={isDraft}
        class:text-red-200={isDeleted}
      >
        {isDeleted ? $_("Deleted") : $_("Draft")}
      </div>
    {/if}

    <DisplayField
      fieldname="id"
      value={otherInvestor.id}
      {model}
      {labelClass}
      {valueClass}
      {wrapperClass}
      showLabel
    />
    <DisplayField
      fieldname="name"
      value={otherInvestor.name}
      {model}
      {labelClass}
      {valueClass}
      {wrapperClass}
      showLabel
      extras={{
        investorNameUnknown: otherInvestor.name_unknown,
      }}
    />
    <DisplayField
      fieldname="country_id"
      value={otherInvestor.country_id}
      {model}
      {labelClass}
      {valueClass}
      {wrapperClass}
      showLabel
    />
    <DisplayField
      fieldname="classification"
      value={otherInvestor.classification}
      {model}
      {labelClass}
      {valueClass}
      {wrapperClass}
      showLabel
    />

    <hr class="m-2 w-2/3" />

    <DisplayField
      fieldname="involvement.relationship"
      value={relationship}
      {model}
      {labelClass}
      {valueClass}
      {wrapperClass}
      showLabel
    />
    <DisplayField
      fieldname="involvement.parent_relation"
      value={involvement.parent_relation}
      {model}
      {labelClass}
      {valueClass}
      {wrapperClass}
      showLabel
    />
    <DisplayField
      fieldname="involvement.investment_type"
      value={involvement.investment_type}
      {model}
      {labelClass}
      {valueClass}
      {wrapperClass}
      showLabel
    />
    <DisplayField
      fieldname="involvement.percentage"
      value={involvement.percentage}
      {model}
      {labelClass}
      {valueClass}
      {wrapperClass}
      showLabel
    />
    <DisplayField
      fieldname="involvement.loans_amount"
      value={involvement.loans_amount}
      {model}
      {labelClass}
      {valueClass}
      {wrapperClass}
      showLabel
      extras={{ currency: involvement.loans_currency_id }}
    />
    <DisplayField
      fieldname="involvement.loans_date"
      value={involvement.loans_date}
      {model}
      {labelClass}
      {valueClass}
      {wrapperClass}
      showLabel
    />
    <DisplayField
      fieldname="involvement.comment"
      value={involvement.comment}
      {model}
      {labelClass}
      {valueClass}
      {wrapperClass}
      showLabel
    />

    <span class="text-left">
      <SourcesDisplayButton model="investor" path={["involvements", involvement.nid]} />
    </span>
  </div>
{:else}
  <div class="bg-red-200 bg-opacity-10 p-2 text-red-200">
    {$_("Invalid investor: {investor_id}", {
      values: { investor_id: otherInvestorId },
    })}
  </div>
{/if}
