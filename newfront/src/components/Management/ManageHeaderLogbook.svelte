<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import { _ } from "svelte-i18n";
  import type { Obj } from "$lib/types/generics";
  import UserSelect from "$components/Management/UserSelect.svelte";
  import ManageHeaderLogbookList from "./ManageHeaderLogbookList.svelte";

  const dispatch = createEventDispatcher();
  export let object: Obj;
  export let objectVersion: number;

  let comment = "";
  let send_to_user;
  let commentArea;

  function addComment() {
    if (!commentArea.checkValidity()) {
      commentArea.reportValidity();
      return;
    }

    dispatch("addComment", { comment, send_to_user });
    comment = "";
  }
</script>

<div class="bg-lm-warmgray lg:w-1/3">
  <h3 class="mx-3">{$_("Logbook")}</h3>
  <div class="mx-1">
    <form action="." method="post">
      <div class="">
        <textarea
          bind:this={commentArea}
          bind:value={comment}
          required
          rows="2"
          class="w-full"
        />
      </div>
      <div class="my-2 ml-1 lg:flex items-center">
        <span class="lg:w-1/5">{$_("Send to")}:</span>
        <div class="flex-grow">
          <UserSelect bind:value={send_to_user} />
        </div>
        <button
          type="button"
          class="btn btn-pelorous btn-slim lg:w-1/5"
          on:click|preventDefault={addComment}
        >
          {$_("Send")}
        </button>
      </div>
    </form>
  </div>

  <ManageHeaderLogbookList workflowinfos={object.workflowinfos} />
</div>

<!--<style lang="scss" scoped>-->
<!--  .comments {-->
<!--    background: #c4c4c4;-->
<!--    padding: 0.7rem;-->
<!--    color: rgba(black, 0.6);-->
<!--    max-height: 100%;-->
<!--    flex-grow: 1;-->
<!--    display: flex;-->
<!--    flex-direction: column;-->

<!--    @media screen and (min-width: 992px) {-->
<!--      max-width: 40vw;-->
<!--    }-->

<!--    h3 {-->
<!--      margin-top: 0;-->
<!--      font-weight: 600;-->
<!--      margin-bottom: 0.2em;-->
<!--      font-size: 1.2em;-->
<!--    }-->

<!--    .new-comment {-->
<!--      font-size: 0.9em;-->
<!--      margin-bottom: 1em;-->

<!--      textarea {-->
<!--        padding: 0.2em 0.5em;-->
<!--        width: 100%;-->
<!--        border: 1px solid lightgrey;-->
<!--        border-radius: 5px;-->
<!--        z-index: 1;-->
<!--        position: relative;-->
<!--        font-size: 0.9em;-->

<!--        &:focus {-->
<!--          border-color: transparent;-->
<!--          outline: none;-->
<!--        }-->
<!--      }-->

<!--      .send {-->
<!--        display: flex;-->
<!--        align-items: center;-->

<!--        span {-->
<!--          white-space: nowrap;-->
<!--          padding-right: 5px;-->
<!--        }-->

<!--        input {-->
<!--          flex: 1;-->
<!--          width: 100px;-->
<!--          margin: 0 2px 0 0.5em;-->
<!--          border: 1px solid lightgrey;-->
<!--          border-radius: 5px;-->
<!--        }-->

<!--        .btn {-->
<!--          margin-left: 7px;-->
<!--          background: var(&#45;&#45;color-lm-investor);-->
<!--          padding: 0.38em 0.7em;-->
<!--          font-size: 0.9em;-->
<!--          border-radius: 5px;-->

<!--          &:hover {-->
<!--            background-color: var(&#45;&#45;color-lm-investor-light);-->
<!--          }-->

<!--          &:focus,-->
<!--          &:active {-->
<!--            outline: none;-->
<!--          }-->
<!--        }-->
<!--      }-->
<!--    }-->
<!--  }-->
<!--</style>-->

<!--<style lang="scss">-->
<!--  .comment .message p:last-child {-->
<!--    margin-bottom: 0;-->
<!--  }-->

<!--  .send {-->
<!--    .multiselect,-->
<!--    .multiselect__tags {-->
<!--      min-height: 30px;-->
<!--    }-->

<!--    .multiselect {-->
<!--      min-width: auto;-->
<!--    }-->

<!--    .multiselect__tags {-->
<!--      padding-top: 4px;-->
<!--      padding-left: 2px;-->
<!--      padding-right: 25px;-->
<!--    }-->

<!--    .multiselect__select {-->
<!--      height: 32px;-->
<!--      width: 32px;-->
<!--      padding-left: 0;-->
<!--      padding-right: 0;-->
<!--    }-->

<!--    .multiselect__placeholder,-->
<!--    .multiselect__single {-->
<!--      margin-bottom: 0 !important;-->
<!--    }-->

<!--    .multiselect__placeholder {-->
<!--      padding-top: 0;-->
<!--      padding-left: 5px;-->
<!--    }-->

<!--    .multiselect__input {-->
<!--      font-size: 1em;-->
<!--      margin-bottom: 2px;-->
<!--    }-->
<!--  }-->
<!--</style>-->
