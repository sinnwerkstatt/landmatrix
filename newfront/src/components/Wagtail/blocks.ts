import Columns1on1Block from "$components/Wagtail/Columns1on1Block.svelte";
import Columns3Block from "$components/Wagtail/Columns3Block.svelte";
import FAQsBlock from "$components/Wagtail/FAQsBlock.svelte";
import FullWidthContainerBlock from "$components/Wagtail/FullWidthContainerBlock.svelte";
import GalleryBlock from "$components/Wagtail/GalleryBlock.svelte";
import HeadingBlock from "$components/Wagtail/HeadingBlock.svelte";
import ImageBlock from "$components/Wagtail/ImageBlock.svelte";
import ParagraphBlock from "$components/Wagtail/ParagraphBlock.svelte";
import RawHTMLBlock from "$components/Wagtail/RawHTMLBlock.svelte";
import ResourcesTeasersBlock from "$components/Wagtail/ResourcesTeasersBlock.svelte";
import SectionDividerBlock from "$components/Wagtail/SectionDividerBlock.svelte";
import SliderBlock from "$components/Wagtail/SliderBlock.svelte";
import TitleBlock from "$components/Wagtail/TitleBlock.svelte";

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
};
