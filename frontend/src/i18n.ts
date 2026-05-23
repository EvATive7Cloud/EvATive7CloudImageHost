import { createI18n } from "vue-i18n";
import en from "./locales/en";
import ja from "./locales/ja";
import zhCN from "./locales/zh-CN";

export const supportedLocales = ["zh-CN", "en", "ja"] as const;
export type SupportedLocale = (typeof supportedLocales)[number];

const messages = {
  "zh-CN": zhCN,
  en,
  ja,
} as const;

const storageKey = "evative7-cloud-image-host:locale";
const fallbackLocale: SupportedLocale = "zh-CN";

function normalizeLocale(locale: string | null | undefined): SupportedLocale | null {
  if (!locale) {
    return null;
  }

  const lowerLocale = locale.toLowerCase();
  if (lowerLocale.startsWith("zh")) {
    return "zh-CN";
  }

  if (lowerLocale.startsWith("en")) {
    return "en";
  }

  if (lowerLocale.startsWith("ja")) {
    return "ja";
  }

  return null;
}

function detectLocale(): SupportedLocale {
  if (typeof window !== "undefined") {
    const savedLocale = normalizeLocale(window.localStorage.getItem(storageKey));
    if (savedLocale) {
      return savedLocale;
    }

    const browserLocale = normalizeLocale(window.navigator.language);
    if (browserLocale) {
      return browserLocale;
    }
  }

  return fallbackLocale;
}

export const i18n = createI18n({
  legacy: false,
  locale: detectLocale(),
  fallbackLocale,
  messages,
});

export function setLocale(locale: SupportedLocale) {
  i18n.global.locale.value = locale;
  if (typeof window !== "undefined") {
    window.localStorage.setItem(storageKey, locale);
  }
}
