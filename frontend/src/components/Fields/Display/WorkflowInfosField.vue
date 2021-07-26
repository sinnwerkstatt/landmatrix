<template>
  <div class="workflowinfo-field" @click="showMore">
    {{ value[0].timestamp | dayjs("YYYY-MM-DD") }}<br />
    <div>
      <span> From {{ value[0].from_user.username }}</span>
      <span v-if="value[0].to_user"> to {{ value[0].to_user.username }}</span>
    </div>
    {{ value[0].comment }}
    <div v-if="moreInfos" class="more-infos">
      <div class="close-x" @mouseup.prevent="closeShowMoreEsc">
        <i class="lm lm-close"></i>
      </div>
      <ManageHeaderCommentsList :workflowinfos="value"></ManageHeaderCommentsList>
    </div>
  </div>
</template>

<script>
  import ManageHeaderCommentsList from "$components/Management/ManageHeaderCommentsList";
  export default {
    components: { ManageHeaderCommentsList },
    props: {
      formfield: { type: Object, required: true },
      value: { type: Array, required: true },
      model: { type: String, required: true },
    },
    data() {
      return { moreInfos: false };
    },
    beforeDestroy() {
      document.removeEventListener("keydown", this.closeShowMoreEsc);
    },
    methods: {
      closeShowMoreEsc(e) {
        if (
          e instanceof MouseEvent ||
          (e instanceof KeyboardEvent && e.key === "Escape")
        ) {
          this.moreInfos = false;
          document.removeEventListener("keydown", this.closeShowMoreEsc);
        }
      },
      showMore() {
        if (!this.moreInfos) {
          this.moreInfos = true;
          document.addEventListener("keydown", this.closeShowMoreEsc);
        } else {
          this.moreInfos = false;
          document.removeEventListener("keydown", this.closeShowMoreEsc);
        }
      },
    },
  };
</script>
<style scoped lang="scss">
  .close-x {
    padding-inline-end: 0.5rem;
    text-align: end;
  }
  .workflowinfo-field {
    cursor: pointer;
    font-size: 0.8rem;
    position: relative;
  }
  .more-infos {
    font-size: 1rem;
    z-index: 1000;
    background: #c4c4c4;
    overflow: hidden;
    position: absolute;
    top: 100%;
    right: 0;
    width: 20em;
    height: 20em;
    //display: none;
  }
</style>
