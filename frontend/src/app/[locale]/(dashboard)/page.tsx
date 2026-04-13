'use client';

import { useTranslations } from 'next-intl';
import { Users, Calendar, Clock, CreditCard } from 'lucide-react';

export default function DashboardPage() {
  const t = useTranslations('nav');

  const cards = [
    { label: t('patients'), value: '--', icon: Users, color: 'bg-teal-500' },
    { label: t('appointments'), value: '--', icon: Calendar, color: 'bg-blue-500' },
    { label: t('queue'), value: '--', icon: Clock, color: 'bg-amber-500' },
    { label: t('billing'), value: '--', icon: CreditCard, color: 'bg-green-500' },
  ];

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">{t('dashboard')}</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {cards.map((card) => (
          <div key={card.label} className="bg-white rounded-xl shadow-sm border border-[var(--color-border)] p-5">
            <div className="flex items-center gap-4">
              <div className={`${card.color} p-3 rounded-lg text-white`}>
                <card.icon size={24} />
              </div>
              <div>
                <p className="text-sm text-[var(--color-text-muted)]">{card.label}</p>
                <p className="text-2xl font-bold">{card.value}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
