// polyfill to make wagtail modeltranslation work
// bug report: https://github.com/infoportugal/wagtail-modeltranslation/issues/390
// internal issue: https://git.sinntern.de/landmatrix/landmatrix/-/issues/651

function cleanForSlug(
  val,
  useURLify,
  { unicodeSlugsEnabled = window.unicodeSlugsEnabled } = {}
) {
  if (useURLify) {
    // URLify performs extra processing on the string (e.g. removing stopwords) and is more suitable
    // for creating a slug from the title, rather than sanitising a slug entered manually
    const cleaned = window.URLify(val, 255);

    // if the result is blank (e.g. because the title consisted entirely of stopwords),
    // fall through to the non-URLify method
    if (cleaned) {
      return cleaned;
    }
  }

  // just do the "replace"
  if (unicodeSlugsEnabled) {
    return val
      .replace(/\s+/g, "-")
      .replace(/[&/\\#,+()$~%.'":`@^!*?<>{}]/g, "")
      .toLowerCase();
  }

  return val
    .replace(/\s+/g, "-")
    .replace(/[^A-Za-z0-9\-_]/g, "")
    .toLowerCase();
}
