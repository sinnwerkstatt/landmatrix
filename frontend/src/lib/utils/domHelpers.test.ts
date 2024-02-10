import { createComponentAsDiv } from "$lib/utils/domHelpers"

import DivDummy from "./TestDivDummy.svelte"
import ScriptDummy from "./TestScriptDummy.svelte"

describe("createComponentAsDiv", () => {
  test("Create div element containing svelte component ", () => {
    const div1 = createComponentAsDiv(DivDummy)
    expect(div1.nodeName).toEqual("DIV")
    expect(div1.children.length).toEqual(1)
    expect(div1.children[0].id).toEqual("div-dummy")

    const div2 = createComponentAsDiv(ScriptDummy)
    expect(div2.nodeName).toEqual("DIV")
    expect(div2.children.length).toEqual(0)
  })
})
