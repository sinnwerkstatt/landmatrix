<script>
  import ColorDef from "./ColorDef.svelte"
  import { allColors } from "./colors"
</script>

<h2 class="display1">Color styles</h2>

<h3 class="heading1">General</h3>

<h4 class="heading3 mt-12">Primary</h4>
<div class="my-6">
  For:
  <ul>
    <li>UI Elements (Buttons etc)</li>
    <li>
      Infographics (Deals), and first choice for sequential and divergent data sets.
    </li>
  </ul>
</div>
<div class="grid grid-cols-3 sm:grid-cols-6">
  <ColorDef title="orange-500" tileColor="bg-lm-orange-500" defs="orange-500" />
  <ColorDef title="orange-400" tileColor="bg-lm-orange-400" defs="orange-400" />
  <ColorDef title="orange-300" tileColor="bg-lm-orange-300" defs="orange-300" />
  <ColorDef title="orange-200" tileColor="bg-lm-orange-200" defs="orange-200" />
  <ColorDef title="orange-100" tileColor="bg-lm-orange-100" defs="orange-100" />
  <ColorDef title="orange-50" tileColor="bg-lm-orange-50" defs="orange-50" />
</div>

<h4 class="heading3 mt-12">Graytones</h4>
<div class="my-6">
  For:
  <ul>
    <li>Text, backgrounds</li>
    <li>Infographics, non-active status or less relevant data</li>
  </ul>
</div>
<div class="grid grid-cols-3 sm:grid-cols-6">
  <ColorDef title="white" tileColor="bg-white" defs="white" />
  <ColorDef title="black" tileColor="bg-lm-black" defs="black" />
  <ColorDef title="gray-dark" tileColor="bg-gray-dark" defs="gray-dark" />
  <ColorDef title="gray-medium" tileColor="bg-gray-medium" defs="gray-medium" />
  <ColorDef title="gray-light" tileColor="bg-gray-light" defs="gray-light" />
</div>

<h4 class="heading3 mt-12">Secondary</h4>
<div class="my-6">
  For:
  <ul>
    <li>UI Elements (Buttons etc)</li>
    <li>
      Infographics (Deals), and first choice for sequential and divergent data sets.
    </li>
  </ul>
</div>
<div class="grid grid-cols-3 sm:grid-cols-6">
  <ColorDef title="main, pelorous-500" tileColor="bg-lm-pelorous" defs="pelorous-500" />
  <ColorDef title="pelorous-400" tileColor="bg-lm-pelorous-400" defs="pelorous-400" />
  <ColorDef title="pelorous-300" tileColor="bg-lm-pelorous-300" defs="pelorous-300" />
  <ColorDef title="pelorous-200" tileColor="bg-lm-pelorous-200" defs="pelorous-200" />
  <ColorDef title="pelorous-100" tileColor="bg-lm-pelorous-100" defs="pelorous-100" />
  <ColorDef title="pelorous-50" tileColor="bg-lm-pelorous-50" defs="pelorous-50" />
</div>

<h4 class="heading3 mt-12">Accent purple</h4>
<div class="grid grid-cols-3 sm:grid-cols-6">
  <ColorDef title="purple-500" tileColor="bg-lm-purple" defs="purple-500" />
  <ColorDef title="purple-400" tileColor="bg-lm-purple-400" defs="purple-400" />
  <ColorDef title="purple-300" tileColor="bg-lm-purple-300" defs="purple-300" />
  <ColorDef title="purple-200" tileColor="bg-lm-purple-200" defs="purple-200" />
  <ColorDef title="purple-100" tileColor="bg-lm-purple-100" defs="purple-100" />
  <ColorDef title="purple-50" tileColor="bg-lm-purple-50" defs="purple-50" />
</div>

<h4 class="heading3 mt-12">Accent violet</h4>
<div class="grid grid-cols-3 sm:grid-cols-6">
  <ColorDef title="violet-500" tileColor="bg-lm-violet" defs="violet-500" />
  <ColorDef title="violet-400" tileColor="bg-lm-violet-400" defs="violet-400" />
  <ColorDef title="violet-300" tileColor="bg-lm-violet-300" defs="violet-300" />
  <ColorDef title="violet-200" tileColor="bg-lm-violet-200" defs="violet-200" />
  <ColorDef title="violet-100" tileColor="bg-lm-violet-100" defs="violet-100" />
  <ColorDef title="violet-50" tileColor="bg-lm-violet-50" defs="violet-50" />
</div>
<h4 class="heading3 mt-12">Accent green</h4>
<div class="grid grid-cols-3 sm:grid-cols-6">
  <ColorDef title="green-500" tileColor="bg-lm-green" defs="green-500" />
  <ColorDef title="green-400" tileColor="bg-lm-green-400" defs="green-400" />
  <ColorDef title="green-300" tileColor="bg-lm-green-300" defs="green-300" />
  <ColorDef title="green-200" tileColor="bg-lm-green-200" defs="green-200" />
  <ColorDef title="green-100" tileColor="bg-lm-green-100" defs="green-100" />
  <ColorDef title="green-50" tileColor="bg-lm-green-50" defs="green-50" />
</div>
<h4 class="heading3 mt-12">Accent red</h4>
<div class="grid grid-cols-3 sm:grid-cols-6">
  <ColorDef title="red-500" tileColor="bg-lm-red" defs="red-500" />
  <ColorDef title="red-400" tileColor="bg-lm-red-400" defs="red-400" />
  <ColorDef title="red-300" tileColor="bg-lm-red-300" defs="red-300" />
  <ColorDef title="red-200" tileColor="bg-lm-red-200" defs="red-200" />
  <ColorDef title="red-100" tileColor="bg-lm-red-100" defs="red-100" />
  <ColorDef title="red-50" tileColor="bg-lm-red-50" defs="red-50" />
</div>
<h4 class="heading3 mt-12">Accent yellow</h4>
<div class="grid grid-cols-3 sm:grid-cols-6">
  <ColorDef title="yellow-500" tileColor="bg-lm-yellow" defs="yellow-500" />
  <ColorDef title="yellow-400" tileColor="bg-lm-yellow-400" defs="yellow-400" />
  <ColorDef title="yellow-300" tileColor="bg-lm-yellow-300" defs="yellow-300" />
  <ColorDef title="yellow-200" tileColor="bg-lm-yellow-200" defs="yellow-200" />
  <ColorDef title="yellow-100" tileColor="bg-lm-yellow-100" defs="yellow-100" />
  <ColorDef title="yellow-50" tileColor="bg-lm-yellow-50" defs="yellow-50" />
</div>

<h3 class="heading1 mt-24">Concepts</h3>

<h4 class="heading3 mt-12">Sequential</h4>
<div class="my-6">
  For:
  <ul>
    <li>Related data to render relative difference in values (e.g produce info map)</li>
  </ul>
</div>
<div class="grid grid-cols-3 sm:grid-cols-6">
  <ColorDef title="orange-400" tileColor="bg-lm-orange-400" defs="orange-400" />
  <ColorDef title="orange-300" tileColor="bg-lm-orange-300" defs="orange-300" />
  <ColorDef title="orange-200" tileColor="bg-lm-orange-200" defs="orange-200" />
  <ColorDef title="orange-100" tileColor="bg-lm-orange-100" defs="orange-100" />
  <ColorDef title="orange-50" tileColor="bg-lm-orange-50" defs="orange-50" />
  <ColorDef title="white" tileColor="bg-white" defs="white" />
</div>

<h4 class="heading3 mt-12">Divergent</h4>
<div class="my-6">
  For:
  <ul>
    <li>
      Related data, if there is zero point or threshold (e.g. increase/decrease of
      hectares)
    </li>
  </ul>
</div>
<div class="grid grid-cols-3 sm:grid-cols-6">
  <ColorDef title="orange-50" tileColor="bg-lm-orange-50" defs="orange-50" />
  <ColorDef title="orange-100" tileColor="bg-lm-orange-100" defs="orange-100" />
  <ColorDef title="orange-200" tileColor="bg-lm-orange-200" defs="orange-200" />
  <ColorDef title="orange-300" tileColor="bg-lm-orange-300" defs="orange-300" />
  <ColorDef title="orange-400" tileColor="bg-lm-orange-400" defs="orange-400" />
</div>
<div class="grid grid-cols-3 sm:grid-cols-6">
  <ColorDef title="pelorous-50" tileColor="bg-lm-pelorous-50" defs="pelorous-50" />
  <ColorDef title="pelorous-100" tileColor="bg-lm-pelorous-100" defs="pelorous-100" />
  <ColorDef title="pelorous-200" tileColor="bg-lm-pelorous-200" defs="pelorous-200" />
  <ColorDef title="pelorous-300" tileColor="bg-lm-pelorous-300" defs="pelorous-300" />
  <ColorDef title="pelorous-400" tileColor="bg-lm-pelorous-400" defs="pelorous-400" />
</div>
<h4 class="heading3 mt-12">System</h4>
<div class="grid grid-cols-3 sm:grid-cols-6">
  <ColorDef title="green-100" tileColor="bg-lm-green-100" defs="green-100" />
  <ColorDef title="green-500" tileColor="bg-lm-green-500" defs="green-500" />
  <ColorDef title="green-700" tileColor="bg-lm-green-700" defs="green-700" />
  <ColorDef title="red-700" tileColor="bg-lm-red-700" defs="red-700" />
  <ColorDef title="red-500" tileColor="bg-lm-red-500" defs="red-500" />
  <ColorDef title="red-100" tileColor="bg-lm-red-100" defs="red-100" />
</div>

<h4 class="heading3 mt-12">Highlight</h4>
<div class="my-6">
  For:
  <ul>
    <li>Highlighting data (e.g. set focus on highest number)</li>
  </ul>
</div>
<div class="grid grid-cols-3 sm:grid-cols-6">
  <ColorDef title="gray-light" tileColor="bg-gray-light" defs="gray-light" />
  <ColorDef title="gray-light" tileColor="bg-gray-light" defs="gray-light" />
  <ColorDef title="gray-light" tileColor="bg-gray-light" defs="gray-light" />
  <ColorDef title="orange-500" tileColor="bg-lm-orange-500" defs="orange-500" />
  <ColorDef title="gray-light" tileColor="bg-gray-light" defs="gray-light" />
  <ColorDef title="gray-light" tileColor="bg-gray-light" defs="gray-light" />
</div>

<h4 class="heading3 mt-12">Categorical</h4>
<div class="my-6">
  For:
  <ul>
    <li>unrelated data, in the above given sequence/priority (e.g. produce)</li>
  </ul>
</div>
<div class="grid grid-cols-3 sm:grid-cols-6">
  <ColorDef title="pelorous-500" tileColor="bg-lm-pelorous-500" defs="pelorous-500" />
  <ColorDef title="purple-500" tileColor="bg-lm-purple-500" defs="purple-500" />
  <ColorDef title="yellow-500" tileColor="bg-lm-yellow-500" defs="yellow-500" />
  <ColorDef title="violet-500" tileColor="bg-lm-violet-500" defs="violet-500" />
  <ColorDef title="green-500" tileColor="bg-lm-green-500" defs="green-500" />
  <ColorDef title="red-500" tileColor="bg-lm-red-500" defs="red-500" />
</div>

<h4 class="heading3 mt-12">Status</h4>
<div class="my-6">
  For:
  <ul>
    <li>
      status, green-tones for active, gray-tones for non active (e.g. negotiation
      status)
    </li>
  </ul>
</div>
<div class="grid grid-cols-3 sm:grid-cols-6">
  <ColorDef title="green-500" tileColor="bg-lm-green-500" defs="green-500" />
  <ColorDef title="green-300" tileColor="bg-lm-green-300" defs="green-300" />
  <ColorDef title="green-100" tileColor="bg-lm-green-100" defs="green-100" />
  <ColorDef title="gray-dark" tileColor="bg-gray-dark" defs="gray-dark" />
  <ColorDef title="gray-medium" tileColor="bg-gray-medium" defs="gray-medium" />
  <ColorDef title="gray-light" tileColor="bg-gray-light" defs="gray-light" />
</div>
