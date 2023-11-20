<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { InvestorHull } from "$lib/types/newtypes.js"

  export let investor: InvestorHull
</script>

<section>
  <div class="mt-2 space-y-4">
    <h3 class="my-0">{$_("Involvements")}</h3>
    {#each investor.involvements as invo}
      <code class="whitespace-pre">{JSON.stringify(invo, null, 2)}</code>
    {/each}
  </div>
</section>

<!--  <h3>{$_("Involvements")} ({simpleInvolvements.length})</h3>-->
<!--  <table class="relative mb-20 w-full table-auto">-->
<!--    <thead class="border-b-2 dark:border-gray-800">-->
<!--      <tr>-->
<!--        <th>{$_("Investor ID")}</th>-->
<!--        <th>{$_("Name")}</th>-->
<!--        <th>{$_("Country of registration")}</th>-->
<!--        <th>{$_("Classification")}</th>-->
<!--        <th>{$_("Relationship")}</th>-->
<!--        <th>{$_("Ownership share")}</th>-->
<!--      </tr>-->
<!--    </thead>-->
<!--    <tbody>-->
<!--      {#each simpleInvolvements as involvement}-->
<!--        <tr-->
<!--          class={involvement.investor.status === Status.DELETED-->
<!--            ? "bg-lm-red-deleted"-->
<!--            : ""}-->
<!--        >-->
<!--          <td>-->
<!--            <DisplayField-->
<!--              value={involvement.investor.id}-->
<!--              valueClasses=""-->
<!--              wrapperClasses="text-center"-->
<!--              fieldname="id"-->
<!--              model="investor"-->
<!--            />-->
<!--          </td>-->
<!--          <td>-->
<!--            <DisplayField-->
<!--              value={involvement.investor.name}-->
<!--              valueClasses=""-->
<!--              wrapperClasses=""-->
<!--              fieldname="name"-->
<!--              model="investor"-->
<!--            />-->
<!--          </td>-->
<!--          <td>-->
<!--            <DisplayField-->
<!--              value={involvement.investor.country}-->
<!--              valueClasses=""-->
<!--              wrapperClasses=""-->
<!--              fieldname="country"-->
<!--              model="investor"-->
<!--            />-->
<!--          </td>-->
<!--          <td>-->
<!--            <DisplayField-->
<!--              value={involvement.investor.classification}-->
<!--              valueClasses=""-->
<!--              wrapperClasses=""-->
<!--              fieldname="classification"-->
<!--              model="investor"-->
<!--            />-->
<!--          </td>-->
<!--          <td>{involvement.role}</td>-->
<!--          <td>-->
<!--            {#if involvement.percentage}-->
<!--              {involvement.percentage} %-->
<!--            {/if}-->
<!--          </td>-->
<!--        </tr>-->
<!--      {/each}-->
<!--    </tbody>-->
<!--  </table>-->

<!--  {#if investor.deals?.length > 0}-->
<!--    <h3>-->
<!--      {$_("Deals (Involvements as Operating company)")} ({investor.deals.length})-->
<!--    </h3>-->

<!--    <table class="relative w-full table-auto">-->
<!--      <thead class="border-b-2">-->
<!--        <tr>-->
<!--          <th>{$_("Deal ID")}</th>-->
<!--          <th>{$_("Target country")}</th>-->
<!--          <th>{$_("Intention of investment")}</th>-->
<!--          <th>{$_("Current negotiation status")}</th>-->
<!--          <th>{$_("Current implementation status")}</th>-->
<!--          <th>{$_("Deal size")}</th>-->
<!--        </tr>-->
<!--      </thead>-->
<!--      <tbody>-->
<!--        {#each investor.deals as deal}-->
<!--          <tr>-->
<!--            {#each ["id", "country", "current_intention_of_investment", "current_negotiation_status", "current_implementation_status", "deal_size"] as field}-->
<!--              <td>-->
<!--                <DisplayField-->
<!--                  value={deal[field]}-->
<!--                  valueClasses=""-->
<!--                  wrapperClasses=""-->
<!--                  fieldname={field}-->
<!--                />-->
<!--              </td>-->
<!--            {/each}-->
<!--          </tr>-->
<!--        {/each}-->
<!--      </tbody>-->
<!--    </table>-->
<!--  {/if}-->
<!--{/if}-->
<!--{#if activeTab === "#data_sources"}-->
<!--  <DealSubmodelSection-->
<!--    model="datasource"-->
<!--    modelName="Data source"-->
<!--    entries={investor.datasources}-->
<!--  />-->
