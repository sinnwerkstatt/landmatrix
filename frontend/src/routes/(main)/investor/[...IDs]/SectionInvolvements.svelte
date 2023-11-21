<script lang="ts">
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import { fieldChoices } from "$lib/stores"
  import type { InvestorHull } from "$lib/types/newtypes.js"

  import CountryField from "$components/Fields/Display2/CountryField.svelte"
  import DecimalField from "$components/Fields/Display2/DecimalField.svelte"
  import IDField from "$components/Fields/Display2/IDField.svelte"
  import TextField from "$components/Fields/Display2/TextField.svelte"

  export let investor: InvestorHull

  $: filteredInvolvements = $page.data.user
    ? investor.involvements
    : investor.involvements.filter(i => !i.other_investor.deleted)
</script>

<section>
  <div class="mb-16 mt-2 space-y-4">
    <h3 class="heading3 my-0">{$_("Involvements")} ({filteredInvolvements.length})</h3>
    <div class="grid gap-4 lg:grid-cols-2 xl:grid-cols-3">
      {#each filteredInvolvements as involvement}
        <div class="flex flex-col gap-1 border border-lm-pelorous p-2">
          <IDField
            label={$_("ID")}
            value={involvement.other_investor.id}
            fieldname="investor.id"
            wrapperClass="flex flex-wrap gap-2 justify-between"
            labelClass="whitespace-nowrap text-gray-dark"
            valueClass=""
          />
          <TextField
            label={$_("Name")}
            value={involvement.other_investor.name}
            fieldname="investor.name"
            wrapperClass="flex flex-wrap gap-2 justify-between"
            labelClass="whitespace-nowrap text-gray-dark"
            valueClass=""
          />
          <CountryField
            label={$_("Country of registration")}
            value={involvement.other_investor.country}
            fieldname="country"
            wrapperClass="flex flex-wrap gap-2 justify-between"
            labelClass="whitespace-nowrap text-gray-dark"
            valueClass=""
          />
          <TextField
            label={$_("Classification")}
            value={involvement.other_investor.classification}
            fieldname="investor.classification"
            choices={$fieldChoices.investor.classification}
            wrapperClass="flex flex-wrap gap-2 justify-between"
            labelClass="whitespace-nowrap text-gray-dark"
            valueClass=""
          />
          ---
          <TextField
            label={$_("Relationship")}
            value={involvement.relationship}
            fieldname="investor.relationship"
            wrapperClass="flex flex-wrap gap-2 justify-between"
            labelClass="whitespace-nowrap text-gray-dark"
            valueClass=""
          />
          <TextField
            label={$_("Investment type")}
            value={involvement.investment_type}
            fieldname="investor.investment_type"
            choices={$fieldChoices.investor.investment_type}
            wrapperClass="flex flex-wrap gap-2 justify-between"
            labelClass="whitespace-nowrap text-gray-dark"
            valueClass=""
          />
          <!--{#if involvement.loans_amount}-->
          <!--  <div class="flex flex-wrap justify-between gap-4">-->
          <!--    <div class="whitespace-nowrap text-gray-dark">{$_("Loan")}</div>-->
          <!--    <div>{involvement.loans_amount} {involvement.loans_currency}</div>-->
          <!--  </div>-->
          <!--{/if}-->

          <DecimalField
            label={$_("Ownership share")}
            value={involvement.percentage}
            fieldname="involvement.percentage"
            wrapperClass="flex flex-wrap gap-2 justify-between"
            labelClass="whitespace-nowrap text-gray-dark"
            valueClass=""
            unit="%"
          />
          <TextField
            label={$_("Comment")}
            value={involvement.comment}
            fieldname="investor.comment"
            wrapperClass="flex flex-wrap gap-2 justify-between"
            labelClass="whitespace-nowrap text-gray-dark"
            valueClass=""
          />
        </div>
      {/each}
    </div>
  </div>
</section>

{#if investor.selected_version.deals.length > 0}
  <section>
    <div class="mb-10 mt-2 space-y-4">
      <h3 class="heading3 my-0">
        {$_("Deals (Involvements as Operating company)")} ({investor.selected_version
          .deals.length})
      </h3>

      <table class="relative w-full table-auto">
        <thead class="border-b-2">
          <tr>
            <th>{$_("Deal ID")}</th>
            <th>{$_("Target country")}</th>
            <th>{$_("Intention of investment")}</th>
            <th>{$_("Current negotiation status")}</th>
            <th>{$_("Current implementation status")}</th>
            <th>{$_("Deal size")}</th>
          </tr>
        </thead>
        <tbody>
          {#each investor.selected_version.deals as deal}
            <tr>
              <td>
                <IDField value={deal.id} fieldname="deal.id" />
              </td>
              <td>
                <CountryField value={deal.country} fieldname="country" />
              </td>
              <td>
                <!--            <TextField-->
                <!--              multipleChoices-->
                <!--              value={deal.selected_version.current_intention_of_investment}-->
                <!--              fieldname="current_intention_of_investment"-->
                <!--              choices={$fieldChoices.deal.intention_of_investment}-->
                <!--            />-->
              </td>
              <td>
                <TextField
                  value={deal.selected_version.current_negotiation_status}
                  fieldname="current_negotiation_status"
                  choices={$fieldChoices.deal.negotiation_status}
                />
              </td>
              <td>
                <TextField
                  value={deal.selected_version.current_implementation_status}
                  fieldname="current_implementation_status"
                  choices={$fieldChoices.deal.implementation_status}
                />
              </td>
              <td>
                <DecimalField
                  value={deal.selected_version.deal_size}
                  fieldname="deal_size"
                  unit={$_("ha")}
                />
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  </section>
{/if}
