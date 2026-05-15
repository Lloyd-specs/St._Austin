'use client';

import { useEffect, useState } from 'react';
import { useTranslations } from 'next-intl';
import { Search, Plus, ChevronLeft, ChevronRight } from 'lucide-react';
import api from '@/lib/api';

interface Patient {
  id: string;
  unique_pid: string;
  first_name: string;
  last_name: string;
  date_of_birth: string;
  sex: string;
  phone_primary: string;
  city: string;
  blood_type: string;
  insurance_provider: string;
}

export default function PatientsPage() {
  const t = useTranslations('patients');
  const tc = useTranslations('common');
  const [patients, setPatients] = useState<Patient[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);

  useEffect(() => {
    setLoading(true);
    const params: Record<string, string> = { page: page.toString() };
    if (search) params.search = search;

    api.get('/patients/', { params })
      .then((res) => {
        setPatients(res.data.results || res.data);
        setTotal(res.data.count || res.data.length || 0);
      })
      .catch(() => setPatients([]))
      .finally(() => setLoading(false));
  }, [page, search]);

  const calculateAge = (dob: string) => {
    const birth = new Date(dob);
    const today = new Date();
    let age = today.getFullYear() - birth.getFullYear();
    const m = today.getMonth() - birth.getMonth();
    if (m < 0 || (m === 0 && today.getDate() < birth.getDate())) age--;
    return age;
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">{t('title')}</h1>
        <button className="flex items-center gap-2 bg-teal-700 hover:bg-teal-800 text-white px-4 py-2.5 rounded-lg text-sm font-medium transition">
          <Plus size={18} />
          {t('newPatient')}
        </button>
      </div>

      {/* Search */}
      <div className="bg-white rounded-xl shadow-sm border border-[var(--color-border)] mb-4">
        <div className="p-4 border-b border-[var(--color-border)]">
          <div className="relative">
            <Search size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input
              type="text"
              placeholder={`${tc('search')} par nom, ID, telephone...`}
              className="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent outline-none"
              value={search}
              onChange={(e) => { setSearch(e.target.value); setPage(1); }}
            />
          </div>
        </div>

        {/* Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-gray-50 text-left">
                <th className="px-4 py-3 font-medium text-gray-600">{t('patientId')}</th>
                <th className="px-4 py-3 font-medium text-gray-600">{t('lastName')}</th>
                <th className="px-4 py-3 font-medium text-gray-600">{t('firstName')}</th>
                <th className="px-4 py-3 font-medium text-gray-600">{t('sex')}</th>
                <th className="px-4 py-3 font-medium text-gray-600">Age</th>
                <th className="px-4 py-3 font-medium text-gray-600">{t('phone')}</th>
                <th className="px-4 py-3 font-medium text-gray-600">{t('bloodType')}</th>
                <th className="px-4 py-3 font-medium text-gray-600">{t('insurance')}</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan={8} className="px-4 py-8 text-center text-gray-500">
                    {tc('loading')}
                  </td>
                </tr>
              ) : patients.length === 0 ? (
                <tr>
                  <td colSpan={8} className="px-4 py-8 text-center text-gray-500">
                    {tc('noResults')}
                  </td>
                </tr>
              ) : (
                patients.map((patient) => (
                  <tr key={patient.id} className="border-t border-gray-100 hover:bg-gray-50 cursor-pointer transition-colors">
                    <td className="px-4 py-3 font-mono text-xs text-teal-700 font-medium">{patient.unique_pid}</td>
                    <td className="px-4 py-3 font-medium">{patient.last_name}</td>
                    <td className="px-4 py-3">{patient.first_name}</td>
                    <td className="px-4 py-3">
                      <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${
                        patient.sex === 'M' ? 'bg-blue-100 text-blue-700' : 'bg-pink-100 text-pink-700'
                      }`}>
                        {patient.sex === 'M' ? 'Homme' : 'Femme'}
                      </span>
                    </td>
                    <td className="px-4 py-3">{calculateAge(patient.date_of_birth)} ans</td>
                    <td className="px-4 py-3 text-gray-600">{patient.phone_primary}</td>
                    <td className="px-4 py-3">
                      {patient.blood_type && (
                        <span className="inline-flex items-center px-2 py-0.5 rounded bg-red-50 text-red-700 text-xs font-medium">
                          {patient.blood_type}
                        </span>
                      )}
                    </td>
                    <td className="px-4 py-3 text-gray-600">{patient.insurance_provider || '-'}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        {total > 0 && (
          <div className="px-4 py-3 border-t border-gray-100 flex items-center justify-between text-sm text-gray-600">
            <span>{total} patient(s)</span>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={page === 1}
                className="p-1.5 rounded hover:bg-gray-100 disabled:opacity-30 disabled:cursor-not-allowed"
              >
                <ChevronLeft size={18} />
              </button>
              <span>Page {page}</span>
              <button
                onClick={() => setPage((p) => p + 1)}
                disabled={patients.length < 10}
                className="p-1.5 rounded hover:bg-gray-100 disabled:opacity-30 disabled:cursor-not-allowed"
              >
                <ChevronRight size={18} />
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
