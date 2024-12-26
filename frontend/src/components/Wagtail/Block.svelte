<script lang="ts" module>
  import Columns1on1Block from "$components/Wagtail/Columns1on1Block.svelte"
  import Columns3Block from "$components/Wagtail/Columns3Block.svelte"
  import DataTeaserBlock from "$components/Wagtail/DataTeaserBlock.svelte"
  import DealCountBlock from "$components/Wagtail/DealCountBlock.svelte"
  import FAQsBlock from "$components/Wagtail/FAQsBlock.svelte"
  import FullWidthContainerBlock from "$components/Wagtail/FullWidthContainerBlock.svelte"
  import GalleryBlock from "$components/Wagtail/GalleryBlock.svelte"
  import HeadingBlock from "$components/Wagtail/HeadingBlock.svelte"
  import ImageBlock from "$components/Wagtail/ImageBlock.svelte"
  import ImageTextBlock from "$components/Wagtail/ImageTextBlock.svelte"
  import NewResourcesTeasersBlock from "$components/Wagtail/NewResourcesTeasersBlock.svelte"
  import ParagraphBlock from "$components/Wagtail/ParagraphBlock.svelte"
  import PartnerBlock from "$components/Wagtail/PartnerBlock.svelte"
  import RawHTMLBlock from "$components/Wagtail/RawHTMLBlock.svelte"
  import ResourcesTeasersBlock from "$components/Wagtail/ResourcesTeasersBlock.svelte"
  import SectionDividerBlock from "$components/Wagtail/SectionDividerBlock.svelte"
  import SliderBlock from "$components/Wagtail/SliderBlock.svelte"
  import TitleBlock from "$components/Wagtail/TitleBlock.svelte"

  //     // eslint-disable-next-line @typescript-eslint/no-explicit-any
  //   export const BLOCK_MAP: { [key: string]: Component<{ value: any }> } = {

  // TODO: Remove unused blocks!

  export const blockMap = {
    columns_1_1: Columns1on1Block,
    columns_3: Columns3Block,
    faqs_block: FAQsBlock,
    full_width_container: FullWidthContainerBlock,
    gallery: GalleryBlock,
    heading: HeadingBlock,
    html: RawHTMLBlock,
    image: ImageBlock,
    linked_image: ImageBlock,
    paragraph: ParagraphBlock,
    resources_teasers: ResourcesTeasersBlock,
    slider: SliderBlock,
    title: TitleBlock,
    section_divider: SectionDividerBlock,
    image_text_block: ImageTextBlock,
    dealcount: DealCountBlock,
    latest_resources: NewResourcesTeasersBlock,
    data_teaser: DataTeaserBlock,
    partners: PartnerBlock,
  }

  export type BlockKey = keyof typeof blockMap
</script>

<script lang="ts">
  import type { WagtailStreamfieldBlock } from "$lib/types/wagtail"

  interface Props {
    block: WagtailStreamfieldBlock
  }

  let { block = $bindable() }: Props = $props()
</script>

{#if blockMap[block.type]}
  {@const SvelteComponent = blockMap[block.type]}
  <SvelteComponent value={block.value} />
{:else}
  <div class="bg-red-100">
    Unknown block: <strong>"{block.type}"</strong>
    <pre class="text-xs">
          {JSON.stringify(block.value, null, 2)}
        </pre>
  </div>
{/if}
