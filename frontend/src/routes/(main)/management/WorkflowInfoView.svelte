<script lang="ts">
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import type { DealHull, InvestorHull } from "$lib/types/newtypes"

  import DateTimeField from "$components/Fields/Display2/DateTimeField.svelte"
  import DisplayField from "$components/Fields/DisplayField.svelte"
  import StarIcon from "$components/icons/StarIcon.svelte"
  import Table from "$components/Table/Table.svelte"

  import type { CreateWorkflowInfoViewFn } from "./workflowViews"
  import {
    createRequestFeedbackView,
    createRequestImprovementView,
    createTodoFeedbackView,
    createTodoImprovementView,
  } from "./workflowViews"

  export let objects: Array<DealHull | InvestorHull>
  export let model: "deal" | "investor" = "deal"

  type TabID =
    | "todo_feedback"
    | "todo_improvement"
    | "requested_feedback"
    | "requested_improvement"
  export let tabId: TabID

  const createObjectsMap: {
    [key in TabID]: CreateWorkflowInfoViewFn
  } = {
    requested_feedback: createRequestFeedbackView,
    requested_improvement: createRequestImprovementView,
    todo_feedback: createTodoFeedbackView,
    todo_improvement: createTodoImprovementView,
  }

  $: createObjects = createObjectsMap[tabId]

  $: columns = [
    { key: "star", label: "", span: 1 },
    { key: "dateOfRequest", label: $_("Date of request"), span: 3 },
    { key: "id", label: $_("ID"), span: 1 },
    { key: "country_id", label: $_("Country"), span: 3 },
    { key: "status", label: $_("Status"), span: 2 }, // TODO Kurt sometimes Mode sometimes Status
    { key: "fromUser", label: $_("From user"), span: 2 },
    { key: "toUser", label: $_("To user"), span: 2 },
    { key: "feedback", label: $_("Feedback"), span: 5 },
  ]
  const wrapperClass = ""
  const valueClass = ""
</script>

<Table
  columns={columns.map(c => c.key)}
  items={createObjects({ page: $page }, objects)}
  labels={columns.map(c => c.label)}
  spans={columns.map(c => c.span)}
>
  <svelte:fragment let:fieldName let:obj slot="field">
    {#if fieldName === "star"}
      {#if obj.openReq}
        <div title={$_("Open request")}>
          <StarIcon />
        </div>
      {/if}
    {:else if fieldName === "dateOfRequest"}
      <DateTimeField
        value={obj.relevantWFI?.timestamp}
        extras={{ format: "YYYY-MM-DD HH:mm" }}
      />
    {:else if fieldName === "id"}
      <DisplayField
        {wrapperClass}
        {valueClass}
        fieldname="id"
        value={obj.id}
        extras={{ objectVersion: obj.draft_version_id }}
        {model}
      />
    {:else if fieldName === "country_id"}
      <DisplayField
        {wrapperClass}
        {valueClass}
        fieldname="country_id"
        value={obj.country_id}
      />
    {:else if fieldName === "status"}
      {obj.mode}
      <!--            <StatusField status={obj.status} draft_status={obj.draft_status} />-->
    {:else if fieldName === "fromUser"}
      <DisplayField
        fieldname="created_by_id"
        value={obj.relevantWFI?.from_user_id}
        {wrapperClass}
        {valueClass}
      />
    {:else if fieldName === "toUser"}
      <DisplayField
        fieldname="created_by_id"
        value={obj.relevantWFI?.to_user_id}
        {wrapperClass}
        {valueClass}
      />
    {:else if fieldName === "feedback"}
      {obj.relevantWFI?.comment}
      <!--      <WorkflowInfosField value={obj.workflowinfos}>-->
      <!--        {obj.relevantWFI?.comment}-->
      <!--      </WorkflowInfosField>-->
    {/if}
  </svelte:fragment>
</Table>
