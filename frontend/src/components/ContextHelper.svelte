<script lang="ts">
  import { createFloatingActions } from "svelte-floating-ui"
  import { autoPlacement, offset, shift } from "svelte-floating-ui/dom"
  import { _ } from "svelte-i18n"
  import { twMerge } from "tailwind-merge"

  import { invalidate } from "$app/navigation"
  import { page } from "$app/stores"

  import type { components } from "$lib/openAPI"
  import { loading } from "$lib/stores/basics"
  import { getCsrfToken } from "$lib/utils"

  import IconXMark from "$components/Accountability/icons/IconXMark.svelte"
  import QuestionMarkCircleIcon from "$components/icons/QuestionMarkCircleIcon.svelte"

  let className = ""
  export { className as class }
  export let identifier: string

  $: editMode = $page.data.user?.is_contexthelp_editor

  $: helpContent = $page.data.contextHelp?.find(x => x.identifier === identifier)

  $: classNames = twMerge(
    "size-4",
    editMode && !helpContent ? "text-red-500" : "text-orange-500",
    className,
  )

  let cHelp: components["schemas"]["ContextHelp"]
  $: cHelp = helpContent ?? {
    identifier: identifier,
    description: "",
    link: "",
  }
  let showOverlay = false

  const [floatingRef, floatingContent] = createFloatingActions({
    strategy: "absolute",
    // placement: "top",
    middleware: [offset(10), shift(), autoPlacement()],
  })

  const onsubmit = async (e: SubmitEvent) => {
    e.preventDefault()
    loading.set(true)

    if (helpContent?.id)
      await $page.data.apiClient.PUT("/api/context_help/{id}/", {
        params: { path: { id: helpContent.id } },
        body: cHelp,
        headers: { "X-CSRFToken": await getCsrfToken() },
      })
    else
      await $page.data.apiClient.POST("/api/context_help/", {
        body: cHelp,
        headers: { "X-CSRFToken": await getCsrfToken() },
      })
    await invalidate("/api/context_help/")
    loading.set(false)
  }
</script>

{#if editMode || helpContent}
  <button on:click={() => (showOverlay = !showOverlay)} use:floatingRef>
    <QuestionMarkCircleIcon class={classNames} />
  </button>
{/if}

{#if showOverlay}
  <div
    class="absolute z-50 mx-2 my-1 min-w-96 rounded border bg-stone-300 px-3 py-2 font-sans text-base font-normal shadow dark:bg-gray-700"
    use:floatingContent
  >
    <div>
      <div><button on:click={() => (showOverlay = false)}><IconXMark /></button></div>
      {#if editMode}
        <form class="flex flex-col gap-4" on:submit={onsubmit}>
          <textarea
            class="inpt"
            bind:value={cHelp.description}
            placeholder="Description"
            rows="10"
          />
          <input class="inpt" bind:value={cHelp.link} type="url" placeholder="URL" />
          <button type="submit" class="btn" disabled={$loading}>{$_("Save")}</button>
        </form>
      {:else}
        <div class="whitespace-pre text-wrap text-left" style="text-wrap: pretty;">
          {helpContent?.description}
        </div>
        {#if helpContent?.link}
          <a target="_blank" class="float-right mt-2" href={helpContent.link}>
            {$_("Read more")}
          </a>
        {/if}
      {/if}
    </div>
  </div>
{/if}
