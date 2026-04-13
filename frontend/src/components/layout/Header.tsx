'use client';

import { useTranslations } from 'next-intl';
import { LogOut } from 'lucide-react';
import { useAuthStore } from '@/store/authSlice';
import { LanguageSwitcher } from '@/components/layout/LanguageSwitcher';

export function Header() {
  const t = useTranslations('auth');
  const tRoles = useTranslations('roles');
  const user = useAuthStore((s) => s.user);
  const logout = useAuthStore((s) => s.logout);

  return (
    <header className="h-16 bg-white border-b border-[var(--color-border)] flex items-center justify-between px-6 flex-shrink-0">
      {/* Left side */}
      <div className="flex items-center gap-2">
        <span className="text-lg font-semibold text-[var(--color-text)]">SIH</span>
      </div>

      {/* Right side */}
      <div className="flex items-center gap-4">
        <LanguageSwitcher />

        {user && (
          <div className="flex items-center gap-3">
            <div className="text-right">
              <p className="text-sm font-medium text-[var(--color-text)]">
                {user.full_name}
              </p>
              <span className="inline-block text-xs px-2 py-0.5 rounded-full bg-[var(--color-primary)]/10 text-[var(--color-primary)] font-medium">
                {tRoles(user.role)}
              </span>
            </div>
            <button
              onClick={logout}
              className="p-2 rounded-lg text-[var(--color-text-muted)] hover:bg-gray-100 hover:text-red-600 transition-colors"
              title={t('logout')}
            >
              <LogOut size={18} />
            </button>
          </div>
        )}
      </div>
    </header>
  );
}
