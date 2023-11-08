<script lang="ts">
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import type { Deal } from "$lib/types/deal"
  import type { Investor } from "$lib/types/investor"

  import DateTimeField from "$components/Fields/Display/DateTimeField.svelte"
  import ForeignKeyField from "$components/Fields/Display/ForeignKeyField.svelte"
  import StatusField from "$components/Fields/Display/StatusField.svelte"
  import WorkflowInfosField from "$components/Fields/Display/WorkflowInfosField.svelte"
  import DisplayField from "$components/Fields/DisplayField.svelte"
  import StarIcon from "$components/icons/StarIcon.svelte"
  import Table from "$components/Table/Table.svelte"

  import {
    createTodoFeedbackView,
    createRequestImprovementView,
    createRequestFeedbackView,
    createTodoImprovementView,
  } from "./workflowViews"
  import type { CreateWorkflowInfoViewFn } from "./workflowViews"

  export let objects: Array<Deal | Investor>
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
    { key: "country", label: $_("Country"), span: 3 },
    { key: "status", label: $_("Status"), span: 2 },
    { key: "fromUser", label: $_("From user"), span: 2 },
    { key: "toUser", label: $_("To user"), span: 2 },
    { key: "feedback", label: $_("Feedback"), span: 5 },
  ]
</script>

<Table
  items={createObjects({ page: $page }, objects)}
  columns={columns.map(c => c.key)}
  labels={columns.map(c => c.label)}
  spans={columns.map(c => c.span)}
>
  <svelte:fragment slot="field" let:obj let:fieldName>
    {#if fieldName === "star"}
      {#if obj.openReq}
        <div title={$_("Open request")}>
          <StarIcon />
        </div>
      {/if}
    {:else if fieldName === "dateOfRequest"}
      <DateTimeField value={obj.relevantWFI?.timestamp} format="YYYY-MM-DD HH:mm" />
    {:else if fieldName === "id"}
      <DisplayField
        wrapperClasses="p-1"
        valueClasses=""
        fieldname="id"
        value={obj.id}
        objectVersion={obj.current_draft_id}
        {model}
      />
    {:else if fieldName === "country"}
      <DisplayField
        wrapperClasses="p-1"
        valueClasses=""
        fieldname="country"
        value={obj.country}
        {model}
      />
    {:else if fieldName === "status"}
      <StatusField status={obj.status} draft_status={obj.draft_status} />
    {:else if fieldName === "fromUser"}
      <ForeignKeyField value={obj.relevantWFI?.from_user} formfield={{}} />
    {:else if fieldName === "toUser"}
      <ForeignKeyField value={obj.relevantWFI?.to_user} formfield={{}} />
    {:else if fieldName === "feedback"}
      <WorkflowInfosField value={obj.workflowinfos}>
        {obj.relevantWFI?.comment}
      </WorkflowInfosField>
    {/if}
  </svelte:fragment>
</Table>
