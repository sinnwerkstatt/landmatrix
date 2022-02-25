import ParagraphBlock from "$components/Wagtail/ParagraphBlock.svelte";
import Columns1on1Block from "$components/Wagtail/Columns1on1Block.svelte";
import HeadingBlock from "$components/Wagtail/HeadingBlock.svelte";
import SliderBlock from "$components/Wagtail/SliderBlock.svelte";
import FullWidthContainerBlock from "$components/Wagtail/FullWidthContainerBlock.svelte";
import Columns3Block from "$components/Wagtail/Columns3Block.svelte";
import FAQsBlock from "$components/Wagtail/FAQsBlock.svelte";
import RawHTMLBlock from "$components/Wagtail/RawHTMLBlock.svelte";

export const blockMap = {
  paragraph: ParagraphBlock,
  columns_1_1: Columns1on1Block,
  columns_3: Columns3Block,
  heading: HeadingBlock,
  slider: SliderBlock,
  full_width_container: FullWidthContainerBlock,
  faqs_block: FAQsBlock,
  html: RawHTMLBlock,
};
