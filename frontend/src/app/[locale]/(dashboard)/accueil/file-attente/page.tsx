'use client';

import { useEffect, useState } from 'react';
import { useTranslations } from 'next-intl';
import { Clock, AlertTriangle } from 'lucide-react';
import api from '@/lib/api';

interface QueueEntry {
  id: string;
  patient_name: string;
  department: string;
  priority: number;
  ticket_number: string;
  status: string;
  check_in_time: string;
  served_by_name: string | null;
}

const PRIORITY_LABELS: Record<number, { label: string; style: string }> = {
  0: { label: 'Normal', style: 'bg-gray-100 text-gray-700' },
  1: { label: 'Urgent', style: 'bg-orange-100 text-orange-700' },
  2: { label: 'Urgence', style: 'bg-red-100 text-red-700' },
};

const STATUS_LABELS: Record<string, { label: string; style: string }> = {
  waiting: { label: 'En attente', style: 'bg-yellow-100 text-yellow-700' },
  called: { label: 'Appele', style: 'bg-blue-100 text-blue-700' },
  serving: { label: 'En consultation', style: 'bg-purple-100 text-purple-700' },
  completed: { label: 'Termine', style: 'bg-green-100 text-green-700' },
  skipped: { label: 'Passe', style: 'bg-gray-100 text-gray-500' },
};

export default function QueuePage() {
  const t = useTranslations('nav');
  const tc = useTranslations('common');
  const [entries, setEntries] = useState<QueueEntry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    api.get('/queue/')
      .then((res) => setEntries(res.data.results || res.data))
      .catch(() => setEntries([]))
      .finally(() => setLoading(false));
  }, []);

  const formatTime = (iso: string) => {
    return new Date(iso).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
  };

  const waitingCount = entries.filter(e => e.status === 'waiting').length;
  const servingCount = entries.filter(e => e.status === 'serving').length;

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">{t('queue')}</h1>

      {/* Summary */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
        <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-4 text-center">
          <p className="text-2xl font-bold text-yellow-700">{waitingCount}</p>
          <p className="text-sm text-yellow-600">En attente</p>
        </div>
        <div className="bg-purple-50 border border-purple-200 rounded-xl p-4 text-center">
          <p className="text-2xl font-bold text-purple-700">{servingCount}</p>
          <p className="text-sm text-purple-600">En consultation</p>
        </div>
        <div className="bg-green-50 border border-green-200 rounded-xl p-4 text-center">
          <p className="text-2xl font-bold text-green-700">{entries.filter(e => e.status === 'completed').length}</p>
          <p className="text-sm text-green-600">Termines</p>
        </div>
      </div>

      {/* Queue list */}
      <div className="bg-white rounded-xl shadow-sm border border-[var(--color-border)]">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-gray-50 text-left">
                <th className="px-4 py-3 font-medium text-gray-600">Ticket</th>
                <th className="px-4 py-3 font-medium text-gray-600">Patient</th>
                <th className="px-4 py-3 font-medium text-gray-600">Service</th>
                <th className="px-4 py-3 font-medium text-gray-600">Priorite</th>
                <th className="px-4 py-3 font-medium text-gray-600">Heure arrivee</th>
                <th className="px-4 py-3 font-medium text-gray-600">Statut</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr><td colSpan={6} className="px-4 py-8 text-center text-gray-500">{tc('loading')}</td></tr>
              ) : entries.length === 0 ? (
                <tr><td colSpan={6} className="px-4 py-8 text-center text-gray-500">File d&apos;attente vide</td></tr>
              ) : (
                entries.map((entry) => (
                  <tr key={entry.id} className="border-t border-gray-100 hover:bg-gray-50">
                    <td className="px-4 py-3 font-mono font-bold text-teal-700">{entry.ticket_number}</td>
                    <td className="px-4 py-3 font-medium">{entry.patient_name}</td>
                    <td className="px-4 py-3 text-gray-600">{entry.department}</td>
                    <td className="px-4 py-3">
                      <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-medium ${PRIORITY_LABELS[entry.priority]?.style || ''}`}>
                        {entry.priority > 0 && <AlertTriangle size={12} />}
                        {PRIORITY_LABELS[entry.priority]?.label || 'Normal'}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-gray-600">
                      <span className="flex items-center gap-1">
                        <Clock size={14} />
                        {formatTime(entry.check_in_time)}
                      </span>
                    </td>
                    <td className="px-4 py-3">
                      <span className={`px-2 py-0.5 rounded text-xs font-medium ${STATUS_LABELS[entry.status]?.style || ''}`}>
                        {STATUS_LABELS[entry.status]?.label || entry.status}
                      </span>
                    </td>
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
