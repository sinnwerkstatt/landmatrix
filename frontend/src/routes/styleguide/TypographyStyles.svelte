<script lang="ts">
  import TypoStyle from "./TypoStyle.svelte"

  const display1 = {
    title: "Display 1",
    mobile: "display1 text-[72px]",
    desktop: "display1 text-[120px]",
    specs: [
      { name: "Font", value: "Oswald", tw: "font-oswald" },
      { name: "Letter Spacing", value: "0px", tw: "tracking-normal" },
      { name: "Weight", value: "Bold", tw: "font-bold" },
      { name: "Text Decoration", value: "None" },
      { name: "Size", value: ["72px", "120px"], tw: "text-[72px] md:text-[120px]" },
      { name: "Paragraph Spacing", value: "0px" },
      { name: "Line Height", value: "125%", tw: "leading-tight" },
      { name: "Case", value: "Original", tw: "normal-case" },
    ],
  }

  const heading1 = {
    title: "Heading 1",
    mobile: "heading1 text-[48px]]",
    desktop: "heading1 text-[60px]",
    specs: [
      { name: "Font", value: "Oswald", tw: "font-oswald" },
      { name: "Letter Spacing", value: "0px", tw: "tracking-normal" },
      { name: "Weight", value: "Bold", tw: "font-bold" },
      { name: "Text Decoration", value: "None" },
      { name: "Size", value: ["48px", "60px"], tw: "text-[48px] md:text-[60px]" },
      { name: "Paragraph Spacing", value: "0px" },
      { name: "Line Height", value: "125%", tw: "leading-tight" },
      { name: "Case", value: "Original", tw: "normal-case" },
    ],
  }

  const heading2 = {
    title: "Heading 2",
    mobile: "heading2 text-[40px]",
    desktop: "heading2 text-[48px]",
    specs: [
      { name: "Font", value: "Oswald", tw: "font-oswald" },
      { name: "Letter Spacing", value: "0px", tw: "tracking-normal" },
      { name: "Weight", value: "Bold", tw: "font-bold" },
      { name: "Text Decoration", value: "None" },
      { name: "Size", value: ["40px", "48px"], tw: "text-[40px] md:text-[48px]" },
      { name: "Paragraph Spacing", value: "0px" },
      { name: "Line Height", value: "125%", tw: "leading-tight" },
      { name: "Case", value: "Original", tw: "normal-case" },
    ],
  }

  const heading3 = {
    title: "Heading 3",
    mobile: "heading3 text-[32px]",
    desktop: "heading3 text-[40px]",
    specs: [
      { name: "Font", value: "Oswald", tw: "font-oswald" },
      { name: "Letter Spacing", value: "0px", tw: "tracking-normal" },
      { name: "Weight", value: "Bold", tw: "font-bold" },
      { name: "Text Decoration", value: "None" },
      { name: "Size", value: ["32px", "40px"], tw: "text-[32px] md:text-[40px]" },
      { name: "Paragraph Spacing", value: "0px" },
      { name: "Line Height", value: "125%", tw: "leading-tight" },
      { name: "Case", value: "Original", tw: "normal-case" },
    ],
  }

  const heading4 = {
    title: "Heading 4",
    mobile: "heading4 text-[28px]",
    desktop: "heading4 text-[32px]",
    specs: [
      { name: "Font", value: "Oswald", tw: "font-oswald" },
      { name: "Letter Spacing", value: "0px", tw: "tracking-normal" },
      { name: "Weight", value: "SemiBold", tw: "font-semibold" },
      { name: "Text Decoration", value: "None" },
      { name: "Size", value: ["28px", "32px"], tw: "text-[28px] md:text-[32px]" },
      { name: "Paragraph Spacing", value: "0px" },
      { name: "Line Height", value: "125%", tw: "leading-tight" },
      { name: "Case", value: "Original", tw: "normal-case" },
    ],
  }

  const heading5 = {
    title: "Heading 5",
    mobile: "heading5 text-[24px]",
    desktop: "heading5 text-[28px]",
    specs: [
      { name: "Font", value: "Oswald", tw: "font-oswald" },
      { name: "Letter Spacing", value: "0px", tw: "tracking-normal" },
      { name: "Weight", value: "Regular", tw: "font-normal" },
      { name: "Text Decoration", value: "None" },
      { name: "Size", value: ["24px", "28px"], tw: "text-[24px] md:text-[28px]" },
      { name: "Paragraph Spacing", value: "0px" },
      { name: "Line Height", value: "125%", tw: "leading-tight" },
      { name: "Case", value: "Original", tw: "normal-case" },
    ],
  }

  const subtitle1 = {
    title: "Subtitle 1",
    mobile: "subtitle1 text-[16px]",
    desktop: "subtitle1 text-[18px]",
    specs: [
      { name: "Font", value: "Open Sans", tw: "font-sans" },
      { name: "Letter Spacing", value: "0px", tw: "tracking-normal" },
      { name: "Weight", value: "Bold", tw: "font-bold" },
      { name: "Text Decoration", value: "None" },
      { name: "Size", value: ["16px", "18px"], tw: "text-[16px] md:text-[18px]" },
      { name: "Paragraph Spacing", value: "0px" },
      { name: "Line Height", value: "125%", tw: "leading-tight" },
      { name: "Case", value: "Original", tw: "normal-case" },
    ],
  }

  const subtitle2 = {
    title: "Subtitle 2",
    mobile: "subtitle2 text-[14px]",
    desktop: "subtitle2 text-[16px]",
    specs: [
      { name: "Font", value: "Open Sans", tw: "font-sans" },
      { name: "Letter Spacing", value: "0px", tw: "tracking-normal" },
      { name: "Weight", value: "Bold", tw: "font-bold" },
      { name: "Text Decoration", value: "None" },
      { name: "Size", value: ["14px", "16px"], tw: "text-[14px] md:text-[16px]" },
      { name: "Paragraph Spacing", value: "0px" },
      { name: "Line Height", value: "125%", tw: "leading-tight" },
      { name: "Case", value: "Original", tw: "normal-case" },
    ],
  }

  const body1 = {
    title: "Body 1",
    mobile: "body1 text-[16px]",
    desktop: "body1 text-[18px]",
    specs: [
      { name: "Font", value: "Open Sans", tw: "font-sans" },
      { name: "Letter Spacing", value: "0px", tw: "tracking-normal" },
      { name: "Weight", value: "Regular", tw: "font-normal" },
      { name: "Text Decoration", value: "None" },
      { name: "Size", value: ["16px", "18px"], tw: "text-[16px] md:text-[18px]" },
      { name: "Paragraph Spacing", value: "0px" },
      { name: "Line Height", value: "125%", tw: "leading-tight" },
      { name: "Case", value: "Original", tw: "normal-case" },
    ],
  }

  const body2 = {
    title: "Body 2",
    mobile: "body2 text-[14px]",
    desktop: "body2 text-[16px]",
    specs: [
      { name: "Font", value: "Open Sans", tw: "font-sans" },
      { name: "Letter Spacing", value: "0px", tw: "tracking-normal" },
      { name: "Weight", value: "Regular", tw: "font-normal" },
      { name: "Text Decoration", value: "None" },
      { name: "Size", value: ["14px", "16px"], tw: "text-[14px] md:text-[16px]" },
      { name: "Paragraph Spacing", value: "0px" },
      { name: "Line Height", value: "125%", tw: "leading-tight" },
      { name: "Case", value: "Original", tw: "normal-case" },
    ],
  }

  const caption = {
    title: "The quick brown fox jumps over the lazy dog",
    mobile: "caption text-[12px]",
    desktop: "caption text-[14px]",
    specs: [
      { name: "Font", value: "Open Sans", tw: "font-sans" },
      { name: "Letter Spacing", value: "5%", tw: "tracking-widest" },
      { name: "Weight", value: "Bold", tw: "font-bold" },
      { name: "Text Decoration", value: "None" },
      { name: "Size", value: ["12px", "14px"], tw: "text-[12px] md:text-[14px]" },
      { name: "Paragraph Spacing", value: "0px" },
      { name: "Line Height", value: "125%", tw: "leading-tight" },
      { name: "Case", value: "Upper", tw: "uppercase" },
    ],
  }
</script>

<h2 class="display1 mb-20">Typography styles</h2>

<TypoStyle val={display1} />
<hr />
<TypoStyle val={heading1} />
<hr />
<TypoStyle val={heading2} />
<hr />
<TypoStyle val={heading3} />
<hr />
<TypoStyle val={heading4} />
<hr />
<TypoStyle val={heading5} />
<hr />
<TypoStyle val={subtitle1} />
<hr />
<TypoStyle val={subtitle2} />
<hr />
<TypoStyle val={body1} />
<hr />
<TypoStyle val={body2} />
<hr />
<TypoStyle val={caption} />
