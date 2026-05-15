'use client';

import { useEffect, useState } from 'react';
import { useTranslations } from 'next-intl';
import { CreditCard, Search } from 'lucide-react';
import api from '@/lib/api';

interface Invoice {
  id: string;
  invoice_number: string;
  patient_name?: string;
  patient?: { first_name: string; last_name: string };
  status: string;
  total: string;
  amount_due: string;
  insurance_coverage: string;
  currency: string;
  due_date: string;
  created_at: string;
}

const STATUS_STYLES: Record<string, string> = {
  draft: 'bg-gray-100 text-gray-700',
  pending: 'bg-yellow-100 text-yellow-700',
  partially_paid: 'bg-orange-100 text-orange-700',
  paid: 'bg-green-100 text-green-700',
  cancelled: 'bg-red-100 text-red-700',
};

const STATUS_LABELS: Record<string, string> = {
  draft: 'Brouillon',
  pending: 'En attente',
  partially_paid: 'Partiel',
  paid: 'Payee',
  cancelled: 'Annulee',
};

export default function BillingPage() {
  const t = useTranslations('nav');
  const tc = useTranslations('common');
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState('');

  useEffect(() => {
    setLoading(true);
    const params: Record<string, string> = {};
    if (statusFilter) params.status = statusFilter;
    api.get('/invoices/', { params })
      .then((res) => setInvoices(res.data.results || res.data))
      .catch(() => setInvoices([]))
      .finally(() => setLoading(false));
  }, [statusFilter]);

  const formatXAF = (amount: string | number) => {
    return new Intl.NumberFormat('fr-CM', { style: 'currency', currency: 'XAF', minimumFractionDigits: 0 }).format(Number(amount));
  };

  const totalPending = invoices
    .filter(i => ['pending', 'partially_paid'].includes(i.status))
    .reduce((sum, i) => sum + Number(i.amount_due), 0);

  const totalPaid = invoices
    .filter(i => i.status === 'paid')
    .reduce((sum, i) => sum + Number(i.total), 0);

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">{t('billing')}</h1>
      </div>

      {/* Summary cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
        <div className="bg-green-50 border border-green-200 rounded-xl p-4">
          <p className="text-sm text-green-600">Total encaisse</p>
          <p className="text-xl font-bold text-green-700">{formatXAF(totalPaid)}</p>
        </div>
        <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-4">
          <p className="text-sm text-yellow-600">Montant en attente</p>
          <p className="text-xl font-bold text-yellow-700">{formatXAF(totalPending)}</p>
        </div>
        <div className="bg-blue-50 border border-blue-200 rounded-xl p-4">
          <p className="text-sm text-blue-600">Total factures</p>
          <p className="text-xl font-bold text-blue-700">{invoices.length}</p>
        </div>
      </div>

      {/* Filter */}
      <div className="mb-4 flex items-center gap-3">
        <CreditCard size={18} className="text-gray-500" />
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-teal-500 outline-none"
        >
          <option value="">Tous les statuts</option>
          <option value="pending">En attente</option>
          <option value="partially_paid">Partiellement payee</option>
          <option value="paid">Payee</option>
          <option value="cancelled">Annulee</option>
        </select>
      </div>

      {/* Table */}
      <div className="bg-white rounded-xl shadow-sm border border-[var(--color-border)]">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-gray-50 text-left">
                <th className="px-4 py-3 font-medium text-gray-600">N° Facture</th>
                <th className="px-4 py-3 font-medium text-gray-600">Patient</th>
                <th className="px-4 py-3 font-medium text-gray-600">Total</th>
                <th className="px-4 py-3 font-medium text-gray-600">Assurance</th>
                <th className="px-4 py-3 font-medium text-gray-600">A payer</th>
                <th className="px-4 py-3 font-medium text-gray-600">Statut</th>
                <th className="px-4 py-3 font-medium text-gray-600">Date</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr><td colSpan={7} className="px-4 py-8 text-center text-gray-500">{tc('loading')}</td></tr>
              ) : invoices.length === 0 ? (
                <tr><td colSpan={7} className="px-4 py-8 text-center text-gray-500">{tc('noResults')}</td></tr>
              ) : (
                invoices.map((inv) => (
                  <tr key={inv.id} className="border-t border-gray-100 hover:bg-gray-50 cursor-pointer">
                    <td className="px-4 py-3 font-mono text-xs text-teal-700 font-medium">{inv.invoice_number}</td>
                    <td className="px-4 py-3 font-medium">{inv.patient_name || `${inv.patient?.last_name} ${inv.patient?.first_name}`}</td>
                    <td className="px-4 py-3 font-medium">{formatXAF(inv.total)}</td>
                    <td className="px-4 py-3 text-gray-600">{Number(inv.insurance_coverage) > 0 ? formatXAF(inv.insurance_coverage) : '-'}</td>
                    <td className="px-4 py-3 font-medium text-red-600">{formatXAF(inv.amount_due)}</td>
                    <td className="px-4 py-3">
                      <span className={`px-2 py-0.5 rounded text-xs font-medium ${STATUS_STYLES[inv.status] || ''}`}>
                        {STATUS_LABELS[inv.status] || inv.status}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-gray-500 text-xs">{new Date(inv.created_at).toLocaleDateString('fr-FR')}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
