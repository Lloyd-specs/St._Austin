'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useLocale } from 'next-intl';
import { useAuthStore } from '@/store/authSlice';
import { Sidebar } from '@/components/layout/Sidebar';
import { Header } from '@/components/layout/Header';
import { OfflineBanner } from '@/components/layout/OfflineBanner';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const locale = useLocale();
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const hydrate = useAuthStore((s) => s.hydrate);
  const [hydrated, setHydrated] = useState(false);

  // First: hydrate auth state from localStorage
  useEffect(() => {
    hydrate();
    setHydrated(true);
  }, [hydrate]);

  // Second: only redirect AFTER hydration is complete
  useEffect(() => {
    if (hydrated && !isAuthenticated) {
      router.push(`/${locale}/login`);
    }
  }, [hydrated, isAuthenticated, router, locale]);

  // Show nothing until we've checked localStorage
  if (!hydrated) {
    return (
      <div className="flex h-screen items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-teal-700"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar />
      <div className="flex flex-col flex-1 overflow-hidden">
        <OfflineBanner />
        <Header />
        <main className="flex-1 overflow-y-auto p-6 bg-[var(--color-bg)]">
          {children}
        </main>
      </div>
    </div>
  );
}
