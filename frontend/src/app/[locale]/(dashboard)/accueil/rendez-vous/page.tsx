'use client';

import { useTranslations } from 'next-intl';

export default function AppointmentsPage() {
  const t = useTranslations('nav');
  const tc = useTranslations('common');

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">{t('appointments')}</h1>
      <div className="bg-white rounded-xl shadow-sm border border-[var(--color-border)] p-8 text-center text-[var(--color-text-muted)]">
        {tc('underDevelopment')}
      </div>
    </div>
  );
}
