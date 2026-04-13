'use client';

import { useRouter, usePathname } from 'next/navigation';
import { useLocale } from 'next-intl';

export function LanguageSwitcher() {
  const router = useRouter();
  const pathname = usePathname();
  const locale = useLocale();

  const toggleLocale = () => {
    const newLocale = locale === 'fr' ? 'en' : 'fr';
    // Replace the locale segment in the URL
    const segments = pathname.split('/');
    segments[1] = newLocale;
    const newPath = segments.join('/');
    router.push(newPath);
  };

  return (
    <button
      onClick={toggleLocale}
      className="px-3 py-1.5 text-sm font-medium rounded-lg border border-[var(--color-border)] hover:bg-gray-50 transition-colors text-[var(--color-text)]"
    >
      {locale === 'fr' ? 'EN' : 'FR'}
    </button>
  );
}
