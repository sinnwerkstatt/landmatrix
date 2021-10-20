import type { Country, ObservatoryPage, Region, WagtailPage } from "$types/wagtail";
import type { User } from "$types/user";
import type { StoreOptions } from "vuex";

interface PageState {
  user: User;
  countries: Country[];
  regions: Region[];
  aboutPages: WagtailPage[];
  observatories: ObservatoryPage[];
  messages: Array<unknown>;
  wagtailPage: WagtailPage;
  title: string;
  searchDescription: string;
  breadcrumbs: [];
  showBreadcrumbs: boolean;
  chartDescriptions: string;
}

export const pageModule: StoreOptions<PageState> = {
  state: {
    user: null as unknown as User,
    countries: [],
    regions: [],
    aboutPages: [],
    observatories: [],
    messages: [],
    wagtailPage: null as unknown as WagtailPage,
    title: "",
    searchDescription: "",
    breadcrumbs: [],
    showBreadcrumbs: true,
    chartDescriptions: "",
  },
  getters: {
    getCountryOrRegion:
      (state: PageState) =>
      ({ type, id }: { [key: string]: string | number }) => {
        const roc =
          type === "region"
            ? state.regions.find((region) => region.id === +id)
            : state.countries.find((countries) => countries.id === +id);
        return roc ? roc : { name: "UNKNOWN" };
      },
    userAuthenticated: (state: PageState): boolean => {
      return state.user && state.user.is_authenticated;
    },
    userInGroup: (state: PageState) => (groups: string[]) => {
      if (!state.user) return false;
      return !!state.user.groups?.find((g) => groups.includes(g.name));
    },
  },
  mutations: {
    setUser(state: PageState, user: User) {
      let role = "No Role";
      if (user && user.groups && user.groups.length) {
        const groupi = user.groups
          .map((g) => g.name)
          .filter((name) => {
            return (
              ["Administrators", "Editors", "Reporters", "Admin"].indexOf(name) > -1
            );
          });

        if (groupi.length) {
          let ret = "";
          if (groupi.includes("Reporters")) ret = "Reporter";
          if (groupi.includes("Editors")) ret = "Editor";
          if (groupi.includes("Administrators")) ret = "Administrator";
          const uri = user.userregionalinfo;
          if (uri) {
            let area = uri.region.map((c) => c.name);
            area = area.concat(uri.country.map((c) => c.name));
            if (area.length) {
              ret = `${ret} of ${area.join(", ")}`;
            }
          }
          role = ret;
        }
        user.bigrole = role;
      }
      state.user = user;
    },
    setCountries(state: PageState, countries: Country[]) {
      state.countries = countries;
    },
    setRegions(state: PageState, regions: Region[]) {
      state.regions = regions;
    },
    setAboutPages(state: PageState, aboutPages: WagtailPage[]) {
      state.aboutPages = aboutPages;
    },
    setObservatories(state: PageState, observatories: ObservatoryPage[]) {
      state.observatories = observatories;
    },
    setChartDescriptions(state: PageState, chartDescriptions) {
      state.chartDescriptions = chartDescriptions;
    },
    setWagtailPage(state: PageState, wagtailPage: WagtailPage) {
      state.wagtailPage = wagtailPage;
    },
    setMessages(state: PageState, messages: string[]) {
      state.messages = messages;
    },
    setTitle(state: PageState, title: string) {
      state.title = title;
    },
    setSearchDescription(state: PageState, description: string) {
      state.searchDescription = description;
    },
    setBreadcrumbs(state: PageState, breadcrumbs) {
      state.breadcrumbs = breadcrumbs;
    },
    breadcrumbBar(state: PageState, visible: boolean) {
      state.showBreadcrumbs = visible;
    },
  },
  actions: {
    async fetchObservatoryPages(context, language = "en") {
      console.log("fetchObservatoryPages", { language });
      const url = `/wagtailapi/v2/pages/?order=title&type=wagtailcms.ObservatoryPage&fields=region,country,short_description`;
      const res = await (await fetch(url)).json();
      context.commit("setObservatories", res.items);
    },
    async fetchAboutPages(context, language = "en") {
      console.debug("fetchAboutPages", { language });
      const url = `/wagtailapi/v2/pages/?order=title&type=wagtailcms.AboutIndexPage`;
      const res = await (await fetch(url)).json();
      const indexPageId = res.items[0].id;

      const pagesUrl = `/wagtailapi/v2/pages/?child_of=${indexPageId}`;
      const res_children = await (await fetch(pagesUrl)).json();
      context.commit("setAboutPages", res_children.items);
    },
    async fetchWagtailPage(context, path) {
      const url = `/wagtailapi/v2/pages/find/?html_path=${path}`;
      const res = await (await fetch(url)).json();
      let breadcrumbs;
      let title;
      if (res.meta.type === "wagtailcms.WagtailRootPage") {
        title = null;
        breadcrumbs = [{ name: "Home" }];
      } else {
        title = res.title;
        breadcrumbs = [{ link: { name: "wagtail" }, name: "Home" }, { name: title }];
      }
      context.commit("setTitle", title);
      context.commit("setBreadcrumbs", breadcrumbs);
      context.commit("setSearchDescription", res.meta.search_description);
      context.commit("setWagtailPage", res);
    },
    setPageContext(context, page_context) {
      context.commit("setTitle", page_context.title);
      context.commit("setBreadcrumbs", page_context.breadcrumbs);
    },
    breadcrumbBar(context, visible: boolean) {
      context.commit("breadcrumbBar", visible);
    },
  },
};
