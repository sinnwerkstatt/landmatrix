<script lang="ts">
  import { gql } from "@urql/svelte"

  import { page } from "$app/stores"

  import type { WorkflowInfo as WFInfo } from "$lib/types/generics"

  import type { FormField } from "$components/Fields/fields"
  import ManageHeaderLogbookList from "$components/Management/ManageHeaderLogbookList.svelte"
  import WorkflowInfo from "$components/Management/WorkflowInfo.svelte"
  import Overlay from "$components/Overlay.svelte"

  export let value: object
  export let formfield: FormField
  export let model: "deal" | "investor" = "deal"
  export let objectId: number | null

  let showMoreInfos = false
  let moreInfos: WFInfo[] = []

  async function showMore() {
    showMoreInfos = !showMoreInfos
    const { data } = await $page.data.urqlClient
      .query<
        | { deal: { workflowinfos: WFInfo[] } }
        | { investor: { workflowinfos: WFInfo[] } }
      >(
        gql`
          query DealWFInfo($id: Int!) {
            ${model} (id: $id, subset: UNFILTERED) {
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
        { id: objectId },
      )
      .toPromise()
    console.log(objectId)
    moreInfos = data.deal.workflowinfos
  }

  //     })
  //     .then(({ data }) => (this.moreInfos = data[this.model].workflowinfos))
  // }
  // // export default Vue.extend({
  //   props: {
  //     formfield: { type: Object, required: true },
  //     value: { type: Array, required: true },
  //     model: { type: String, required: true },
  //     objectId: { type: Number, default: null, required: false },
  //   },
  //   beforeDestroy() {
  //     document.removeEventListener("keydown", this.closeShowMoreEsc);
  //   },
  //   methods: {

  //     showMore() {
  //       if (!this.showMoreInfos) {
  //         apolloClient
  //           .query({
  //             query: gql`
  //               query DealWFInfo($id: Int!) {
  //                 ${this.model} (id: $id, subset: UNFILTERED) {
  //                   id
  //                   workflowinfos {
  //                     id
  //                     comment
  //                     timestamp
  //                     from_user {
  //                       id
  //                       username
  //                     }
  //                     to_user {
  //                       id
  //                       username
  //                     }
  //                     draft_status_after
  //                     draft_status_before
  //                   }
  //                 }
  //               }
  //             `,
  //             variables: { id: this.objectId },
  //           })
  //           .then(({ data }) => (this.moreInfos = data[this.model].workflowinfos));
  //         this.showMoreInfos = true;
  //         document.addEventListener("keydown", this.closeShowMoreEsc);
  //       } else {
  //         this.showMoreInfos = false;
  //         document.removeEventListener("keydown", this.closeShowMoreEsc);
  //       }
  //     },
  //   },
  // });
</script>

<div class="workflowinfo-field" on:click={() => showMore()}>
  <WorkflowInfo info={value[0]} />
  <div class="more-infos-anchor">
    {#if showMoreInfos}
      <div class="more-infos">
        <div class="close-x" />
      </div>
    {/if}
  </div>
</div>
<Overlay visible={showMoreInfos} on:close title={`Logbook ${model} ${objectId}`}>
  <ManageHeaderLogbookList workflowinfos={moreInfos} />
</Overlay>

<!--<style lang="scss" scoped>-->
<!--  .workflowinfo-field {-->
<!--    cursor: pointer;-->
<!--    font-size: 0.8rem;-->
<!--  }-->
<!--  .more-infos-anchor {-->
<!--    /* we use an extra div here, for table z-index problems in Management on scroll */-->
<!--    position: relative;-->
<!--  }-->
<!--  .more-infos {-->
<!--    font-size: 1rem;-->
<!--    z-index: 1000;-->
<!--    background: #c4c4c4;-->
<!--    overflow: hidden;-->
<!--    position: absolute;-->
<!--    top: 100%;-->
<!--    right: 0;-->
<!--    width: 20em;-->
<!--    max-height: 20em;-->
<!--    //display: none;-->

<!--    .close-x {-->
<!--      padding-inline-end: 0.5rem;-->
<!--      text-align: end;-->
<!--    }-->
<!--  }-->
<!--</style>-->
