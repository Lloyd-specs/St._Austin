'use client';

import { useEffect, useState } from 'react';
import { useTranslations } from 'next-intl';
import { Users, Calendar, Clock, CreditCard, TrendingUp, AlertTriangle } from 'lucide-react';
import api from '@/lib/api';

interface DashboardData {
  patients_total: number;
  patients_today: number;
  appointments_today: number;
  queue_waiting: number;
  invoices_pending: number;
  revenue_today: number;
}

export default function DashboardPage() {
  const t = useTranslations('nav');
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/dashboard/overview/')
      .then((res) => setData(res.data))
      .catch(() => {
        // Fallback: count from individual endpoints
        Promise.all([
          api.get('/patients/').catch(() => ({ data: { count: 0 } })),
          api.get('/appointments/?scheduled_date=' + new Date().toISOString().split('T')[0]).catch(() => ({ data: { count: 0 } })),
        ]).then(([patients, appointments]) => {
          setData({
            patients_total: patients.data.count || patients.data.results?.length || 0,
            patients_today: 0,
            appointments_today: appointments.data.count || appointments.data.results?.length || 0,
            queue_waiting: 0,
            invoices_pending: 0,
            revenue_today: 0,
          });
        });
      })
      .finally(() => setLoading(false));
  }, []);

  const cards = [
    {
      label: t('patients'),
      value: loading ? '...' : (data?.patients_total?.toLocaleString() || '0'),
      subtitle: loading ? '' : `+${data?.patients_today || 0} aujourd'hui`,
      icon: Users,
      color: 'bg-teal-500',
    },
    {
      label: t('appointments'),
      value: loading ? '...' : (data?.appointments_today?.toString() || '0'),
      subtitle: "Aujourd'hui",
      icon: Calendar,
      color: 'bg-blue-500',
    },
    {
      label: t('queue'),
      value: loading ? '...' : (data?.queue_waiting?.toString() || '0'),
      subtitle: 'En attente',
      icon: Clock,
      color: 'bg-amber-500',
    },
    {
      label: t('billing'),
      value: loading ? '...' : `${(data?.invoices_pending || 0)}`,
      subtitle: 'Factures en attente',
      icon: CreditCard,
      color: 'bg-green-500',
    },
  ];

  const formatXAF = (amount: number) => {
    return new Intl.NumberFormat('fr-CM', { style: 'currency', currency: 'XAF', minimumFractionDigits: 0 }).format(amount);
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">{t('dashboard')}</h1>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {cards.map((card) => (
          <div key={card.label} className="bg-white rounded-xl shadow-sm border border-[var(--color-border)] p-5">
            <div className="flex items-center gap-4">
              <div className={`${card.color} p-3 rounded-lg text-white`}>
                <card.icon size={24} />
              </div>
              <div>
                <p className="text-sm text-[var(--color-text-muted)]">{card.label}</p>
                <p className="text-2xl font-bold">{card.value}</p>
                <p className="text-xs text-[var(--color-text-muted)]">{card.subtitle}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Revenue & Quick Info */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow-sm border border-[var(--color-border)] p-6">
          <div className="flex items-center gap-2 mb-4">
            <TrendingUp size={20} className="text-green-600" />
            <h2 className="text-lg font-semibold">Revenus du jour</h2>
          </div>
          <p className="text-3xl font-bold text-green-600">
            {loading ? '...' : formatXAF(data?.revenue_today || 0)}
          </p>
          <p className="text-sm text-[var(--color-text-muted)] mt-1">Total encaisse aujourd&apos;hui</p>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-[var(--color-border)] p-6">
          <div className="flex items-center gap-2 mb-4">
            <AlertTriangle size={20} className="text-amber-600" />
            <h2 className="text-lg font-semibold">Alertes</h2>
          </div>
          <ul className="space-y-2 text-sm">
            <li className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-amber-500"></span>
              {loading ? '...' : `${data?.invoices_pending || 0} factures en attente de paiement`}
            </li>
            <li className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-blue-500"></span>
              {loading ? '...' : `${data?.queue_waiting || 0} patients en file d'attente`}
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}
