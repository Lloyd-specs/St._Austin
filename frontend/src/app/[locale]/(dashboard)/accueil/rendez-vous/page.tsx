'use client';

import { useEffect, useState } from 'react';
import { useTranslations } from 'next-intl';
import { Calendar, Plus, Clock } from 'lucide-react';
import api from '@/lib/api';

interface Appointment {
  id: string;
  patient_name: string;
  doctor_name: string;
  department: string;
  scheduled_date: string;
  scheduled_time: string;
  status: string;
  reason: string;
}

const STATUS_STYLES: Record<string, string> = {
  scheduled: 'bg-gray-100 text-gray-700',
  confirmed: 'bg-blue-100 text-blue-700',
  checked_in: 'bg-yellow-100 text-yellow-700',
  in_progress: 'bg-purple-100 text-purple-700',
  completed: 'bg-green-100 text-green-700',
  cancelled: 'bg-red-100 text-red-700',
  no_show: 'bg-orange-100 text-orange-700',
};

const STATUS_LABELS: Record<string, string> = {
  scheduled: 'Planifie',
  confirmed: 'Confirme',
  checked_in: 'Arrive',
  in_progress: 'En cours',
  completed: 'Termine',
  cancelled: 'Annule',
  no_show: 'Absent',
};

export default function AppointmentsPage() {
  const t = useTranslations('nav');
  const tc = useTranslations('common');
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [loading, setLoading] = useState(true);
  const [dateFilter, setDateFilter] = useState(new Date().toISOString().split('T')[0]);

  useEffect(() => {
    setLoading(true);
    api.get('/appointments/', { params: { scheduled_date: dateFilter } })
      .then((res) => setAppointments(res.data.results || res.data))
      .catch(() => setAppointments([]))
      .finally(() => setLoading(false));
  }, [dateFilter]);

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">{t('appointments')}</h1>
        <button className="flex items-center gap-2 bg-teal-700 hover:bg-teal-800 text-white px-4 py-2.5 rounded-lg text-sm font-medium transition">
          <Plus size={18} />
          Nouveau rendez-vous
        </button>
      </div>

      <div className="mb-4 flex items-center gap-3">
        <Calendar size={18} className="text-gray-500" />
        <input
          type="date"
          value={dateFilter}
          onChange={(e) => setDateFilter(e.target.value)}
          className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-teal-500 outline-none"
        />
        <button
          onClick={() => setDateFilter(new Date().toISOString().split('T')[0])}
          className="text-sm text-teal-700 hover:text-teal-800 font-medium"
        >
          Aujourd&apos;hui
        </button>
      </div>

      <div className="space-y-3">
        {loading ? (
          <div className="bg-white rounded-xl shadow-sm border border-[var(--color-border)] p-8 text-center text-gray-500">
            {tc('loading')}
          </div>
        ) : appointments.length === 0 ? (
          <div className="bg-white rounded-xl shadow-sm border border-[var(--color-border)] p-8 text-center text-gray-500">
            Aucun rendez-vous pour cette date
          </div>
        ) : (
          appointments.map((apt) => (
            <div key={apt.id} className="bg-white rounded-xl shadow-sm border border-[var(--color-border)] p-4 hover:shadow-md transition-shadow cursor-pointer">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className="flex items-center gap-1 text-gray-500 min-w-[70px]">
                    <Clock size={14} />
                    <span className="text-sm font-medium">{apt.scheduled_time?.slice(0, 5)}</span>
                  </div>
                  <div className="h-10 w-px bg-gray-200"></div>
                  <div>
                    <p className="font-medium">{apt.patient_name}</p>
                    <p className="text-sm text-gray-500">
                      {apt.department} &bull; Dr. {apt.doctor_name} &bull; {apt.reason}
                    </p>
                  </div>
                </div>
                <span className={`px-3 py-1 rounded-full text-xs font-medium ${STATUS_STYLES[apt.status] || 'bg-gray-100'}`}>
                  {STATUS_LABELS[apt.status] || apt.status}
                </span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
