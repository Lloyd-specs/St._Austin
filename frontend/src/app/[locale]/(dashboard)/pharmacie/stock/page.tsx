'use client';

import { useEffect, useState } from 'react';
import { useTranslations } from 'next-intl';
import { Package, Search, AlertTriangle } from 'lucide-react';
import api from '@/lib/api';

interface Medication {
  id: string;
  code: string;
  name: string;
  generic_name: string;
  form: string;
  strength: string;
  category: string;
  unit_price: string;
  manufacturer: string;
  is_active: boolean;
}

const FORM_LABELS: Record<string, string> = {
  tablet: 'Comprime',
  capsule: 'Gelule',
  syrup: 'Sirop',
  injection: 'Injectable',
  cream: 'Creme',
  drops: 'Gouttes',
  inhaler: 'Inhalateur',
  suppository: 'Suppositoire',
};

export default function StockPage() {
  const t = useTranslations('nav');
  const tc = useTranslations('common');
  const [medications, setMedications] = useState<Medication[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  useEffect(() => {
    setLoading(true);
    const params: Record<string, string> = {};
    if (search) params.search = search;

    api.get('/medications/', { params })
      .then((res) => setMedications(res.data.results || res.data))
      .catch(() => setMedications([]))
      .finally(() => setLoading(false));
  }, [search]);

  const formatXAF = (amount: string | number) => {
    return new Intl.NumberFormat('fr-CM', { style: 'currency', currency: 'XAF', minimumFractionDigits: 0 }).format(Number(amount));
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">{t('stock')}</h1>
      </div>

      {/* Search */}
      <div className="mb-4">
        <div className="relative max-w-md">
          <Search size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
          <input
            type="text"
            placeholder="Rechercher un medicament..."
            className="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent outline-none"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
      </div>

      {/* Table */}
      <div className="bg-white rounded-xl shadow-sm border border-[var(--color-border)]">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-gray-50 text-left">
                <th className="px-4 py-3 font-medium text-gray-600">Code</th>
                <th className="px-4 py-3 font-medium text-gray-600">Medicament</th>
                <th className="px-4 py-3 font-medium text-gray-600">DCI</th>
                <th className="px-4 py-3 font-medium text-gray-600">Forme</th>
                <th className="px-4 py-3 font-medium text-gray-600">Dosage</th>
                <th className="px-4 py-3 font-medium text-gray-600">Categorie</th>
                <th className="px-4 py-3 font-medium text-gray-600">Fabricant</th>
                <th className="px-4 py-3 font-medium text-gray-600">Prix unitaire</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr><td colSpan={8} className="px-4 py-8 text-center text-gray-500">{tc('loading')}</td></tr>
              ) : medications.length === 0 ? (
                <tr><td colSpan={8} className="px-4 py-8 text-center text-gray-500">{tc('noResults')}</td></tr>
              ) : (
                medications.map((med) => (
                  <tr key={med.id} className="border-t border-gray-100 hover:bg-gray-50 cursor-pointer">
                    <td className="px-4 py-3 font-mono text-xs text-teal-700 font-medium">{med.code}</td>
                    <td className="px-4 py-3 font-medium">{med.name}</td>
                    <td className="px-4 py-3 text-gray-600">{med.generic_name}</td>
                    <td className="px-4 py-3">
                      <span className="px-2 py-0.5 rounded bg-blue-50 text-blue-700 text-xs font-medium">
                        {FORM_LABELS[med.form] || med.form}
                      </span>
                    </td>
                    <td className="px-4 py-3">{med.strength}</td>
                    <td className="px-4 py-3 text-gray-600">{med.category}</td>
                    <td className="px-4 py-3 text-gray-500 text-xs">{med.manufacturer}</td>
                    <td className="px-4 py-3 font-medium">{formatXAF(med.unit_price)}</td>
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
