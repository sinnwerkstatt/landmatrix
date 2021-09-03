<template>
  <div class="comments-list">
    <div v-for="wfi in workflowinfos" :key="wfi.id">
      <WorkflowInfo :info="wfi"></WorkflowInfo>
    </div>
  </div>
</template>

<script>
  import WorkflowInfo from "$components/Management/WorkflowInfo";

  export default {
    name: "ManageHeaderCommentsList",
    components: { WorkflowInfo },
    props: {
      workflowinfos: { type: Array, required: true },
    },
  };
</script>

<style scoped lang="scss">
  .comments-list {
    cursor: default;
    background: #c4c4c4;
    overflow-y: scroll;
    margin-right: -0.7rem;
    height: 100%;
    box-shadow: inset 0 3px 7px -3px rgba(0, 0, 0, 0.1),
      inset 0px -2px 5px -2px rgba(0, 0, 0, 0.1);
    padding: 2px 4px;
    //margin-left: -4px;
    max-height: 330px;
  }
</style>
