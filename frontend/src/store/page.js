import axios from "axios";

export const pageModule = {
  state: () => ({
    user: null,
    countries: [],
    regions: [],
    aboutPages: [],
    observatories: [],
    messages: [],
    wagtailPage: null,
    title: null,
    searchDescription: null,
    breadcrumbs: [],
    showBreadcrumbs: true,
    chartDescriptions: [],
  }),
  getters: {
    getCountryOrRegion: (state) => ({ type, id }) => {
      let roc =
        type === "region"
          ? state.regions.find((region) => region.id === +id)
          : state.countries.find((countries) => countries.id === +id);

      if (!roc) {
        roc = {
          name: "UNKNOWN",
        };
      }

      return roc;
    },
    userAuthenticated: (state) => {
      return !!(state.user && state.user.is_authenticated);
    },
  },
  mutations: {
    setUser(state, user) {
      let role = "No Role";
      if (user && user.groups && user.groups.length) {
        let groupi = user.groups
          .map((g) => g.name)
          .filter((name) => {
            return (
              ["Administrators", "Editors", "Reporters", "Admin"].indexOf(name) > -1
            );
          });

        if (groupi.length) {
          let ret = "";
          if (groupi.indexOf("Reporters") > -1) ret = "Reporter";
          if (groupi.indexOf("Editors") > -1) ret = "Editor";
          if (groupi.indexOf("Administrators") > -1) ret = "Administrator";
          let uri = user.userregionalinfo;
          if (uri) {
            let area = uri.region.map((c) => c.name);
            area = area.concat(uri.country.map((c) => c.name));
            if (area.length) {
              return `${ret} of ${area.join(", ")}`;
            }
          }
          role = ret;
        }
        user.role = role;
      }
      state.user = user;
    },
    setCountries(state, countries) {
      state.countries = countries;
    },
    setRegions(state, regions) {
      state.regions = regions;
    },
    setAboutPages(state, aboutPages) {
      state.aboutPages = aboutPages;
    },
    setObservatories(state, observatories) {
      state.observatories = observatories;
    },
    setChartDescriptions(state, chartDescriptions) {
      state.chartDescriptions = chartDescriptions;
    },
    setWagtailPage(state, wagtailPage) {
      state.wagtailPage = wagtailPage;
    },
    setMessages(state, messages) {
      state.messages = messages;
    },
    setTitle(state, title) {
      state.title = title;
    },
    setSearchDescription(state, description) {
      state.searchDescription = description;
    },
    setBreadcrumbs(state, breadcrumbs) {
      state.breadcrumbs = breadcrumbs;
    },
    breadcrumbBar(state, visible) {
      state.showBreadcrumbs = visible;
    },
  },
  actions: {
    fetchObservatoryPages(context) {
      return new Promise(function (resolve, reject) {
        let url = `/wagtailapi/v2/pages/?order=title&type=wagtailcms.ObservatoryPage&fields=region,country,short_description`;
        axios
          .get(url)
          .then((response) => {
            context.commit("setObservatories", response.data.items);
            resolve();
          })
          .catch(() => {
            reject();
          });
      });
    },
    fetchAboutPages(context) {
      return new Promise(function (resolve, reject) {
        let indexUrl = `/wagtailapi/v2/pages/?order=title&type=wagtailcms.AboutIndexPage`;
        axios
          .get(indexUrl)
          .then((response) => {
            let indexPageId = response.data.items[0].id;
            let pagesUrl = `/wagtailapi/v2/pages/?child_of=${indexPageId}`;
            axios
              .get(pagesUrl)
              .then((response) => {
                context.commit("setAboutPages", response.data.items);
                resolve();
              })
              .catch(() => {
                reject();
              });
          })
          .catch(() => {
            reject();
          });
      });
    },
    fetchWagtailPage(context, path) {
      let url = `/wagtailapi/v2/pages/find/?html_path=${path}`;
      return new Promise(function (resolve, reject) {
        axios.get(url).then(
          (response) => {
            let breadcrumbs;
            let title;
            if (response.data.meta.type === "wagtailcms.WagtailRootPage") {
              title = null;
              breadcrumbs = [{ name: "Home" }];
            } else {
              title = response.data.title;
              breadcrumbs = [
                { link: { name: "wagtail" }, name: "Home" },
                { name: title },
              ];
            }
            context.commit("setTitle", title);
            context.commit("setBreadcrumbs", breadcrumbs);
            context.commit(
              "setSearchDescription",
              response.data.meta.search_description
            );
            context.commit("setWagtailPage", response.data);
            resolve();
          },
          () => {
            reject();
          }
        );
      });
    },
    setPageContext(context, page_context) {
      context.commit("setTitle", page_context.title);
      context.commit("setBreadcrumbs", page_context.breadcrumbs);
    },
    breadcrumbBar(context, visible) {
      context.commit("breadcrumbBar", visible);
    },
  },
};
