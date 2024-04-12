<script lang="ts">
  import { _ } from "svelte-i18n"
  import Select from "svelte-select"

  import { goto } from "$app/navigation"

  interface SearchResultEntry {
    id: number
    href: string
    country_name: string | null
    type: "deal" | "investor"
    name: string
    name_unknown: boolean
  }

  const loadOptions = async (filterText: string) => {
    if (filterText.length < 2) return []

    const ret = await fetch(`/api/quick_search/?q=${filterText}`)
    const retJson = await ret.json()
    return retJson.items
  }

  let filterText = ""

  const onSelect = (e: CustomEvent<SearchResultEntry>) => {
    console.log(e.detail)
    goto(e.detail.href)
    // filterText = ""
  }

  const makeName = (itm: SearchResultEntry) => {
    if (itm.type === "deal") {
      if (itm.country_name) return `#${itm.id} ${$_("in")} ${itm.country_name}`
      return `#${itm.id}`
    } else if (itm.type === "investor") {
      if (itm.name_unknown)
        return `<span class="italic">[${$_("unknown investor")}]</span> #${itm.id}`
      return `${itm.name} #${itm.id}`
    }
    return "PROBLEMS!"
  }
</script>

<Select
  bind:filterText
  clearFilterTextOnBlur={false}
  itemId="id"
  listAutoWidth={false}
  {loadOptions}
  on:select={onSelect}
  placeholder="Deals and Investors"
>
  <div class="min-w-[20rem] px-2 py-1" slot="empty">
    This search is matching on deal IDs, investor IDs and investor names.
  </div>
  <!--    <div slot="list" let:filteredItems>asdf</div>-->
  <div
    class={item.type === "deal" ? "navbar-item deal" : "navbar-item investor"}
    let:item
    slot="item"
  >
    <a
      class:investor={item.type === "investor"}
      class:opacity-40={item.type === "deal" && !item.is_public}
      href={item.href}
    >
      {@html makeName(item)}
    </a>
  </div>

  <div let:selection slot="selection">
    {@html makeName(selection)}
  </div>
</Select>
