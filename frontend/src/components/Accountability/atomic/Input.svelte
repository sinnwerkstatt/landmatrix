<script lang="ts">
  import { preventNonNumericalInput } from "$lib/accountability/inputHelpers"

  import IconCheck from "../icons/IconCheck.svelte"
  import IconChevron from "../icons/IconChevron.svelte"
  import IconEye from "../icons/IconEye.svelte"
  import IconSearch from "../icons/IconSearch.svelte"
  import IconUser from "../icons/IconUser.svelte"
  import IconXMark from "../icons/IconXMark.svelte"
  import Avatar from "./Avatar.svelte"
  import Badge from "./Badge.svelte"
  import DropdownMenu from "./DropdownMenu.svelte"
  import InputCheckboxGroup from "./InputCheckboxGroup.svelte"

  export let type: "text" | "textarea" | "number" | "radio" | "select" | "multiselect" =
    "text"
  export let choices: {
    value: string
    label: string
    icon?: "check" | "eye"
    color?: "green" | "orange"
  }[] = []
  export let categories: { label: string; values: string[] } = undefined
  export let value
  export let resetButton = true
  export let badgeType: "tag" | "avatar" = "tag"
  export let style: "neutral" | "white" = "neutral"

  export let readonlyCategories = false
  export let label = ""
  export let placeholder = "Placeholder"
  export let icon: "" | "search" | "user" = ""
  export let status: "neutral" | "valid" | "invalid" = "neutral"
  export let message: string | undefined = undefined
  export let disabled = false
  export let search = true

  export let extraClass = ""

  export let inputColor = ""

  // Type textarea
  export let maxlength = 280
  export let rows = 4

  // Type number
  export let unit: string = "ha"
  export let min: string = ""
  export let max: string = ""
  export let step: string = "100"

  // Type select
  const choicesLengthLimit = 1000

  // Locales
  let open = false
  let filter = ""
  let dropdown

  const icons = [
    { icon: "", component: false },
    { icon: "search", component: IconSearch },
    { icon: "user", component: IconUser },
  ]

  const selectIcons = [
    { icon: "check", component: IconCheck },
    { icon: "eye", component: IconEye },
  ]

  // Functions
  function reset() {
    value = ""
    status = "neutral"
  }

  function useScrollIntoView(target) {
    target.scrollIntoView({ behavior: "smooth" })
  }

  function searchMatch(string: string, filter: string) {
    return string.toLowerCase().indexOf(filter.toLowerCase()) >= 0
  }

  function getInputColor(value) {
    let res = ""
    if (type == "select" && value) {
      const choice = choices?.find(c => c.value == value)
      if (choice.color) res = choice.color
    }
    return res
  }

  $: inputColor = getInputColor(value)
</script>

<div class={style == "white" ? "white" : ""}>
  <!-- Label -->
  {#if label}
    <h3 class="my-2 text-a-sm font-medium">{label}</h3>
  {/if}

  <div
    class:disabled
    class="{inputColor} {status} wrapper wrapper-grid {type == 'textarea'
      ? 'h-32'
      : ''}"
  >
    <!-- Icon -->
    {#if icon != ""}
      <span>
        <svelte:component this={icons.find(e => e.icon == icon)?.component} size="24" />
      </span>
    {/if}

    <!-- Input -->
    {#if type == "text"}
      <input
        {disabled}
        type="text"
        name="name"
        {placeholder}
        bind:value
        class="col-span-2 w-full bg-transparent"
        class:noIcon={icon == "" ? true : false}
      />
    {:else if type == "textarea"}
      <textarea
        {disabled}
        name="name"
        {placeholder}
        bind:value
        autocomplete="off"
        {maxlength}
        class="col-span-3 col-start-1 box-border h-full w-full resize-none bg-transparent"
      />
    {:else if type == "multiselect"}
      <button
        {disabled}
        on:click={() => {
          open = !open
        }}
        class="pseudo-input w-full bg-transparent text-left"
        class:noIcon={icon == "" ? true : false}
      >
        <span class="placeholder">{placeholder}</span>
      </button>
    {:else if type == "select"}
      <button
        {disabled}
        on:focus={() => {
          open = !open
        }}
        on:click={() => {
          open = !open
        }}
        class="pseudo-input w-full bg-transparent text-left"
        class:noIcon={icon == "" ? true : false}
        class:extraButton={value && resetButton ? true : false}
      >
        {#if value}
          <span>
            {choices.find(e => e.value == value)?.label}
          </span>
        {:else}
          <span class="placeholder">{placeholder}</span>
        {/if}
      </button>
    {:else if type == "number"}
      <input
        {disabled}
        type="number"
        name="name"
        pattern="[0-9]+"
        {placeholder}
        bind:value
        {min}
        {max}
        {step}
        class="noIcon w-full bg-transparent"
        on:keypress={preventNonNumericalInput}
      />
    {/if}

    <!-- Right item -->
    {#if type == "text"}
      <button {disabled} on:click={reset}><IconXMark /></button>
    {/if}

    {#if type == "multiselect" || type == "select"}
      <button
        {disabled}
        on:click={() => {
          open = !open
        }}
        class="rotate-180"
      >
        <IconChevron />
      </button>
    {/if}

    {#if type == "select" && resetButton && value}
      <button {disabled} on:click={reset}><IconXMark /></button>
    {/if}

    {#if type == "number"}
      <span>{unit}</span>
    {/if}
  </div>

  {#if message}
    <p class="message mt-1.5 text-sm {status}">{message}</p>
  {/if}

  <!-- Dropdown menu for select or multiselect -->
  {#if ["select", "multiselect"].includes(type) && !disabled && open}
    <DropdownMenu
      extraClass="pb-4 absolute z-10 w-[13.5rem] {extraClass}"
      visible={open}
    >
      {#if search}
        <div class="wrapper wrapper-grid m-4">
          <span><IconSearch /></span>
          <input
            {disabled}
            type="text"
            name="name"
            placeholder="Search"
            class="w-full bg-transparent"
            bind:value={filter}
          />
          <button
            {disabled}
            class="text-red"
            on:click={() => {
              filter = ""
            }}
          >
            <IconXMark />
          </button>
        </div>
      {/if}

      <div
        class="max-h-80 overflow-auto {search ? '' : 'pt-4'}"
        bind:this={dropdown}
        use:useScrollIntoView
      >
        {#if type == "multiselect"}
          {#if choices.length > choicesLengthLimit}
            <!-- If too many choices, hide until search is as least 3 characters long -->
            {#if filter.length > 0}
              <InputCheckboxGroup
                {choices}
                {categories}
                bind:group={value}
                {filter}
                {readonlyCategories}
              />
            {:else}
              <p class="px-4 italic text-a-gray-400">Start typing to search</p>
            {/if}
          {:else}
            <!-- Show all choices if less than 1000 (performance OK) -->
            <InputCheckboxGroup
              {choices}
              {categories}
              bind:group={value}
              {filter}
              {readonlyCategories}
            />
          {/if}
        {:else}
          <!-- Type "select" -->
          <div class="flex flex-col">
            {#each choices as choice}
              {@const hidden = !searchMatch(choice.label, filter)}
              <label
                class="flex cursor-pointer items-center gap-2 px-4 py-2 hover:bg-a-gray-100"
                {hidden}
              >
                <input
                  type="radio"
                  name="selection"
                  value={choice.value}
                  bind:group={value}
                  class="appearance-none"
                />
                {#if choice.icon}
                  <span class="icon {choice.color ? choice.color : ''}">
                    <svelte:component
                      this={selectIcons.find(e => e.icon == choice.icon)?.component}
                      size="18"
                    />
                  </span>
                {/if}
                {choice.label}
              </label>
            {/each}
          </div>
        {/if}
      </div>
    </DropdownMenu>
  {/if}

  <!-- Badges for multiselect -->
  {#if type == "multiselect" && value instanceof Array && value.length > 0}
    <div class="mt-2 flex flex-wrap gap-1 {badgeType == 'avatar' ? 'flex-col' : ''} ">
      {#each value as val}
        {@const element = choices.find(e => e.value == val)}
        {#if badgeType == "avatar"}
          <Avatar
            type="base"
            button={true}
            label={element?.label}
            padding={true}
            initials={element?.initials}
            {disabled}
            on:click={() => {
              value = value.filter(v => v != val)
            }}
          />
        {:else}
          <Badge
            color="neutral"
            button={true}
            {disabled}
            label={element?.label}
            on:click={() => {
              value = value.filter(v => v != val)
            }}
          />
        {/if}
      {/each}
    </div>
  {/if}
</div>

<style>
  input,
  textarea,
  .pseudo-input {
    @apply relative z-0;
    @apply outline-none;
    @apply col-span-2;
  }

  input.extraButton,
  .pseudo-input.extraButton {
    @apply col-span-1;
  }

  input.noIcon,
  .pseudo-input.noIcon {
    @apply col-span-3 col-start-1;
  }

  input.noIcon.extraButton,
  .pseudo-input.noIcon.extraButton {
    @apply col-span-2 col-start-1;
  }

  .wrapper-grid {
    display: grid;
    grid-template-columns: 16px auto 16px 16px;
    @apply items-center gap-x-2.5;
  }

  .wrapper {
    @apply h-12;
    @apply min-w-32;
    @apply rounded-lg border px-4 py-2;
    @apply bg-a-gray-50;
    @apply border-a-gray-300;
  }

  .wrapper .white {
    @apply bg-white;
  }

  .wrapper.green {
    @apply bg-a-success-50;
    @apply border-a-success-700;
  }

  .wrapper.orange {
    @apply bg-a-primary-50;
    @apply border-a-primary-500;
  }

  .wrapper::placeholder,
  .wrapper .placeholder {
    @apply line-clamp-1;
  }

  .wrapper::placeholder,
  .wrapper .placeholder,
  .wrapper > span,
  .wrapper > button {
    @apply text-a-gray-400;
  }

  .white .wrapper::placeholder,
  .white .wrapper .placeholder,
  .white .wrapper > span,
  .white .wrapper > button {
    @apply text-a-gray-900;
  }

  .wrapper:focus-within {
    @apply border-a-gray-900;
  }

  .wrapper.disabled,
  .wrapper.disabled > span,
  .wrapper.disabled > button {
    @apply text-a-gray-400;
  }

  .wrapper.disabled > button {
    @apply cursor-default;
  }

  .wrapper.valid,
  .wrapper.valid > span,
  .wrapper.valid > button {
    @apply bg-a-success-50 text-a-success-500;
  }

  .wrapper.valid,
  .wrapper.valid:focus-within {
    @apply border-a-success-500;
  }

  .message.valid {
    @apply text-a-success-500;
  }

  .wrapper.invalid,
  .wrapper.invalid > span,
  .wrapper.invalid > button {
    @apply bg-a-error-50 text-a-error-500;
  }

  .wrapper.invalid,
  .wrapper.invalid:focus-within {
    @apply border-a-error-500;
  }

  .message.invalid {
    @apply text-a-error-500;
  }

  label.hide {
    @apply hidden;
  }

  .icon.green {
    @apply text-a-success-900;
  }
  .icon.orange {
    @apply text-a-warning-500;
  }
</style>
