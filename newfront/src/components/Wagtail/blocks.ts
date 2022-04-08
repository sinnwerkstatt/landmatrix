import Columns1on1Block from "$components/Wagtail/Columns1on1Block.svelte";
import Columns3Block from "$components/Wagtail/Columns3Block.svelte";
import FAQsBlock from "$components/Wagtail/FAQsBlock.svelte";
import FullWidthContainerBlock from "$components/Wagtail/FullWidthContainerBlock.svelte";
import GalleryBlock from "$components/Wagtail/GalleryBlock.svelte";
import HeadingBlock from "$components/Wagtail/HeadingBlock.svelte";
import ImageBlock from "$components/Wagtail/ImageBlock.svelte";
import ParagraphBlock from "$components/Wagtail/ParagraphBlock.svelte";
import RawHTMLBlock from "$components/Wagtail/RawHTMLBlock.svelte";
import SliderBlock from "$components/Wagtail/SliderBlock.svelte";
import TitleBlock from "$components/Wagtail/TitleBlock.svelte";

export const blockMap = {
  paragraph: ParagraphBlock,
  columns_1_1: Columns1on1Block,
  columns_3: Columns3Block,
  heading: HeadingBlock,
  slider: SliderBlock,
  full_width_container: FullWidthContainerBlock,
  faqs_block: FAQsBlock,
  html: RawHTMLBlock,
  image: ImageBlock,
  linked_image: ImageBlock,
  title: TitleBlock,
  gallery: GalleryBlock,
};
