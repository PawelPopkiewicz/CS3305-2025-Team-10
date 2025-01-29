/* eslint-disable */
import * as Router from 'expo-router';

export * from 'expo-router';

declare module 'expo-router' {
  export namespace ExpoRouter {
    export interface __routes<T extends string | object = string> {
      hrefInputParams: { pathname: Router.RelativePathString, params?: Router.UnknownInputParams } | { pathname: Router.ExternalPathString, params?: Router.UnknownInputParams } | { pathname: `/`; params?: Router.UnknownInputParams; } | { pathname: `/_sitemap`; params?: Router.UnknownInputParams; } | { pathname: `${'/(tabs)'}/HomeScreen` | `/HomeScreen`; params?: Router.UnknownInputParams; } | { pathname: `${'/(tabs)'}/MapScreen` | `/MapScreen`; params?: Router.UnknownInputParams; } | { pathname: `${'/(tabs)'}/SearchScreen` | `/SearchScreen`; params?: Router.UnknownInputParams; } | { pathname: `/config/Colors`; params?: Router.UnknownInputParams; } | { pathname: `/screens/map`; params?: Router.UnknownInputParams; } | { pathname: `/screens/search`; params?: Router.UnknownInputParams; };
      hrefOutputParams: { pathname: Router.RelativePathString, params?: Router.UnknownOutputParams } | { pathname: Router.ExternalPathString, params?: Router.UnknownOutputParams } | { pathname: `/`; params?: Router.UnknownOutputParams; } | { pathname: `/_sitemap`; params?: Router.UnknownOutputParams; } | { pathname: `${'/(tabs)'}/HomeScreen` | `/HomeScreen`; params?: Router.UnknownOutputParams; } | { pathname: `${'/(tabs)'}/MapScreen` | `/MapScreen`; params?: Router.UnknownOutputParams; } | { pathname: `${'/(tabs)'}/SearchScreen` | `/SearchScreen`; params?: Router.UnknownOutputParams; } | { pathname: `/config/Colors`; params?: Router.UnknownOutputParams; } | { pathname: `/screens/map`; params?: Router.UnknownOutputParams; } | { pathname: `/screens/search`; params?: Router.UnknownOutputParams; };
      href: Router.RelativePathString | Router.ExternalPathString | `/${`?${string}` | `#${string}` | ''}` | `/_sitemap${`?${string}` | `#${string}` | ''}` | `${'/(tabs)'}/HomeScreen${`?${string}` | `#${string}` | ''}` | `/HomeScreen${`?${string}` | `#${string}` | ''}` | `${'/(tabs)'}/MapScreen${`?${string}` | `#${string}` | ''}` | `/MapScreen${`?${string}` | `#${string}` | ''}` | `${'/(tabs)'}/SearchScreen${`?${string}` | `#${string}` | ''}` | `/SearchScreen${`?${string}` | `#${string}` | ''}` | `/config/Colors${`?${string}` | `#${string}` | ''}` | `/screens/map${`?${string}` | `#${string}` | ''}` | `/screens/search${`?${string}` | `#${string}` | ''}` | { pathname: Router.RelativePathString, params?: Router.UnknownInputParams } | { pathname: Router.ExternalPathString, params?: Router.UnknownInputParams } | { pathname: `/`; params?: Router.UnknownInputParams; } | { pathname: `/_sitemap`; params?: Router.UnknownInputParams; } | { pathname: `${'/(tabs)'}/HomeScreen` | `/HomeScreen`; params?: Router.UnknownInputParams; } | { pathname: `${'/(tabs)'}/MapScreen` | `/MapScreen`; params?: Router.UnknownInputParams; } | { pathname: `${'/(tabs)'}/SearchScreen` | `/SearchScreen`; params?: Router.UnknownInputParams; } | { pathname: `/config/Colors`; params?: Router.UnknownInputParams; } | { pathname: `/screens/map`; params?: Router.UnknownInputParams; } | { pathname: `/screens/search`; params?: Router.UnknownInputParams; };
    }
  }
}
