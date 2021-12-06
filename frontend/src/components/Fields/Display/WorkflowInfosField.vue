<template>
  <div class="workflowinfo-field" @click="showMore">
    <WorkflowInfo :info="value[0]" />
    <div class="more-infos-anchor">
      <div v-if="showMoreInfos" class="more-infos">
        <div class="close-x" @mouseup.prevent="closeShowMoreEsc">
          <i class="lm lm-close"></i>
        </div>
        <ManageHeaderCommentsList :workflowinfos="moreInfos" />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
  import Vue from "vue";
  import gql from "graphql-tag";
  import ManageHeaderCommentsList from "$components/Management/ManageHeaderCommentsList.vue";
  import WorkflowInfo from "$components/Management/WorkflowInfo.vue";
  import { apolloClient } from "$utils/apolloclient";

  export default Vue.extend({
    components: { WorkflowInfo, ManageHeaderCommentsList },
    props: {
      formfield: { type: Object, required: true },
      value: { type: Array, required: true },
      model: { type: String, required: true },
      objectId: { type: Number, default: null, required: false },
    },
    data() {
      return { showMoreInfos: false, moreInfos: [] };
    },
    beforeDestroy() {
      document.removeEventListener("keydown", this.closeShowMoreEsc);
    },
    methods: {
      closeShowMoreEsc(e: Event) {
        if (
          e instanceof MouseEvent ||
          (e instanceof KeyboardEvent && e.key === "Escape")
        ) {
          this.showMoreInfos = false;
          document.removeEventListener("keydown", this.closeShowMoreEsc);
        }
      },
      showMore() {
        if (!this.showMoreInfos) {
          apolloClient
            .query({
              query: gql`
                query DealWFInfo($id: Int!) {
                  ${this.model} (id: $id, subset: UNFILTERED) {
                    id
                    workflowinfos {
                      id
                      comment
                      timestamp
                      from_user {
                        id
                        username
                      }
                      to_user {
                        id
                        username
                      }
                      draft_status_after
                      draft_status_before
                    }
                  }
                }
              `,
              variables: { id: this.objectId },
            })
            .then(({ data }) => (this.moreInfos = data[this.model].workflowinfos));
          this.showMoreInfos = true;
          document.addEventListener("keydown", this.closeShowMoreEsc);
        } else {
          this.showMoreInfos = false;
          document.removeEventListener("keydown", this.closeShowMoreEsc);
        }
      },
    },
  });
</script>
<style lang="scss" scoped>
  .workflowinfo-field {
    cursor: pointer;
    font-size: 0.8rem;
  }
  .more-infos-anchor {
    /* we use an extra div here, for table z-index problems in Management on scroll */
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
    max-height: 20em;
    //display: none;

    .close-x {
      padding-inline-end: 0.5rem;
      text-align: end;
    }
  }
</style>
