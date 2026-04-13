'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useTranslations } from 'next-intl';
import { useLocale } from 'next-intl';
import { useAuthStore } from '@/store/authSlice';
import {
  Users,
  Calendar,
  Clock,
  CreditCard,
  Stethoscope,
  FileText,
  FlaskConical,
  Package,
  Pill,
  ShieldCheck,
  BarChart3,
  UserCog,
  Settings,
  ChevronLeft,
  ChevronRight,
} from 'lucide-react';
import type { LucideIcon } from 'lucide-react';

interface NavItem {
  label: string;
  href: string;
  icon: LucideIcon;
}

interface NavSection {
  title: string;
  items: NavItem[];
  roles: string[];
}

export function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);
  const pathname = usePathname();
  const t = useTranslations('nav');
  const locale = useLocale();
  const user = useAuthStore((s) => s.user);
  const userRole = user?.role || '';

  const sections: NavSection[] = [
    {
      title: t('reception'),
      roles: ['accueil', 'medecin', 'infirmier', 'directeur', 'admin_systeme'],
      items: [
        { label: t('patients'), href: `/${locale}/accueil/patients`, icon: Users },
        { label: t('appointments'), href: `/${locale}/accueil/rendez-vous`, icon: Calendar },
        { label: t('queue'), href: `/${locale}/accueil/file-attente`, icon: Clock },
        { label: t('billing'), href: `/${locale}/accueil/facturation`, icon: CreditCard },
      ],
    },
    {
      title: t('medicalRecords'),
      roles: ['medecin', 'infirmier', 'admin_systeme'],
      items: [
        { label: t('consultations'), href: `/${locale}/dpi/consultations`, icon: Stethoscope },
        { label: t('prescriptions'), href: `/${locale}/dpi/ordonnances`, icon: FileText },
        { label: t('laboratory'), href: `/${locale}/dpi/resultats`, icon: FlaskConical },
      ],
    },
    {
      title: t('pharmacy'),
      roles: ['pharmacien', 'admin_systeme'],
      items: [
        { label: t('stock'), href: `/${locale}/pharmacie/stock`, icon: Package },
        { label: t('dispensation'), href: `/${locale}/pharmacie/dispensation`, icon: Pill },
        { label: t('pharmacheck'), href: `/${locale}/pharmacie/pharmacheck`, icon: ShieldCheck },
      ],
    },
    {
      title: t('direction'),
      roles: ['directeur', 'admin_systeme'],
      items: [
        { label: t('reports'), href: `/${locale}/direction`, icon: BarChart3 },
      ],
    },
    {
      title: t('admin'),
      roles: ['admin_systeme'],
      items: [
        { label: t('users'), href: `/${locale}/admin/utilisateurs`, icon: UserCog },
        { label: t('settings'), href: `/${locale}/admin/parametres`, icon: Settings },
      ],
    },
  ];

  const visibleSections = sections.filter((section) =>
    section.roles.includes(userRole)
  );

  const isActive = (href: string) => pathname === href;

  return (
    <aside
      className={`${
        collapsed ? 'w-16' : 'w-64'
      } bg-[var(--color-sidebar)] text-white flex flex-col transition-all duration-300 ease-in-out flex-shrink-0`}
    >
      {/* Logo area */}
      <div className="h-16 flex items-center justify-between px-4 border-b border-white/10">
        {!collapsed && (
          <span className="text-lg font-bold tracking-wide">SIH</span>
        )}
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="p-1.5 rounded-lg hover:bg-white/10 transition-colors ml-auto"
          aria-label={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          {collapsed ? <ChevronRight size={18} /> : <ChevronLeft size={18} />}
        </button>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto py-4 px-2">
        {visibleSections.map((section) => (
          <div key={section.title} className="mb-5">
            {!collapsed && (
              <p className="px-3 mb-2 text-xs font-semibold uppercase tracking-wider text-white/40">
                {section.title}
              </p>
            )}
            <ul className="space-y-0.5">
              {section.items.map((item) => {
                const active = isActive(item.href);
                return (
                  <li key={item.href}>
                    <Link
                      href={item.href}
                      className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                        active
                          ? 'bg-white/15 text-white'
                          : 'text-white/70 hover:bg-white/8 hover:text-white'
                      } ${collapsed ? 'justify-center' : ''}`}
                      title={collapsed ? item.label : undefined}
                    >
                      <item.icon size={20} className="flex-shrink-0" />
                      {!collapsed && <span>{item.label}</span>}
                    </Link>
                  </li>
                );
              })}
            </ul>
          </div>
        ))}
      </nav>
    </aside>
  );
}
