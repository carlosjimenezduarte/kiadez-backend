const SEARCH_FORM_SELECTOR = "form.topbar-search";
const SEARCH_INPUT_SELECTOR = 'input[type="search"]';
const FEED_SEARCH_PATH = "/feed.html";
const SEARCH_PARAM_KEY = "search";

const normalizeSearchValue = (value) =>
  String(value || "")
    .replace(/\s+/g, " ")
    .trim();

const readCurrentSearchFromLocation = () => {
  const params = new URLSearchParams(window.location.search);
  return normalizeSearchValue(params.get(SEARCH_PARAM_KEY));
};

const buildFeedSearchPath = (query) => {
  const url = new URL(FEED_SEARCH_PATH, window.location.origin);
  if (query) {
    url.searchParams.set(SEARCH_PARAM_KEY, query);
  }
  return `${url.pathname}${url.search}`;
};

export function initTopbarSearch() {
  const cleanups = [];
  let observer = null;

  const wireForm = (form) => {
    if (!form || form.dataset.topbarSearchBound === "1") return;
    const input = form.querySelector(SEARCH_INPUT_SELECTOR);
    if (!input) return;

    form.dataset.topbarSearchBound = "1";

    const currentSearch = readCurrentSearchFromLocation();
    if (currentSearch && !normalizeSearchValue(input.value)) {
      input.value = currentSearch;
    }

    const handleSubmit = (event) => {
      event.preventDefault();
      const query = normalizeSearchValue(input.value);
      if (!query) return;
      window.location.assign(buildFeedSearchPath(query));
    };

    form.addEventListener("submit", handleSubmit);
    cleanups.push(() => form.removeEventListener("submit", handleSubmit));
  };

  const discoverForms = () => {
    document.querySelectorAll(SEARCH_FORM_SELECTOR).forEach((formNode) => wireForm(formNode));
  };

  discoverForms();

  observer = new MutationObserver(() => {
    discoverForms();
  });
  observer.observe(document.body, { childList: true, subtree: true });

  return () => {
    cleanups.forEach((cleanup) => cleanup());
    if (observer) observer.disconnect();
  };
}
