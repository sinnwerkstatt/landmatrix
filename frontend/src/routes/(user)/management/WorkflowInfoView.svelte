<script lang="ts">
  import { _ } from "svelte-i18n"

  import { page } from "$app/state"

  import type { DealHull, InvestorHull } from "$lib/types/data"

  import DateTimeField from "$components/Fields/Display2/DateTimeField.svelte"
  import DisplayField from "$components/Fields/DisplayField.svelte"
  import StarIcon from "$components/icons/StarIcon.svelte"
  import Table, { type Column } from "$components/Table/Table.svelte"

  import type { CreateWorkflowInfoViewFn } from "./workflowViews"
  import {
    createRequestFeedbackView,
    createRequestImprovementView,
    createTodoFeedbackView,
    createTodoImprovementView,
  } from "./workflowViews"

  type TabID =
    | "todo_feedback"
    | "todo_improvement"
    | "requested_feedback"
    | "requested_improvement"
  interface Props {
    objects: Array<DealHull | InvestorHull>
    model?: "deal" | "investor"
    tabId: TabID
  }

  let { objects, model = "deal", tabId }: Props = $props()

  const createObjectsMap: {
    [key in TabID]: CreateWorkflowInfoViewFn
  } = {
    requested_feedback: createRequestFeedbackView,
    requested_improvement: createRequestImprovementView,
    todo_feedback: createTodoFeedbackView,
    todo_improvement: createTodoImprovementView,
  }

  let createObjects = $derived(createObjectsMap[tabId])

  let columns: Column[] = $derived([
    { key: "star", label: "", colSpan: 1 },
    {
      key: "timestamp",
      label: $_("Date of request"),
      colSpan: 3,
      submodel: "relevantWFI",
    },
    { key: "id", label: $_("ID"), colSpan: 1 },
    {
      key: "country_id",
      label: $_("Country"),
      colSpan: 3,
      submodel: model === "investor" ? "selected_version" : undefined,
    },
    { key: "status", label: $_("Status"), colSpan: 2 },
    {
      key: "from_user_id",
      label: $_("From user"),
      colSpan: 2,
      submodel: "relevantWFI",
    },
    { key: "to_user_id", label: $_("To user"), colSpan: 2, submodel: "relevantWFI" },
    { key: "comment", label: $_("Feedback"), colSpan: 5, submodel: "relevantWFI" },
  ])

  const wrapperClass = ""
  const valueClass = ""

  type fieldType = {
    fieldName: string
    obj: DealHull | InvestorHull
  }
</script>

<Table {columns} items={createObjects({ page: page }, objects)}>
  {#snippet field({ fieldName, obj }: fieldType)}
    {@const col = columns.find(c => c.key === fieldName)}

    {#if col?.key === "star"}
      {#if obj.openReq}
        <div title={$_("Open request")}>
          <StarIcon />
        </div>
      {/if}
    {:else if col?.key === "timestamp"}
      <DateTimeField
        value={obj.relevantWFI?.timestamp}
        extras={{ format: "YYYY-MM-DD HH:mm" }}
      />
    {:else if ["from_user_id", "to_user_id"].includes(col.key)}
      <DisplayField
        fieldname="created_by_id"
        value={obj.relevantWFI?.[col.key]}
        {wrapperClass}
        {valueClass}
      />
    {:else if col?.key === "comment"}
      {obj.relevantWFI?.comment}
    {:else if col}
      <DisplayField
        fieldname={col.key}
        value={col.submodel ? obj[col.submodel][col.key] : obj[col.key]}
        {wrapperClass}
        {valueClass}
        {model}
        extras={col.key === "id"
          ? { model, objectVersion: obj.draft_version_id }
          : undefined}
      />
    {/if}
  {/snippet}
</Table>
