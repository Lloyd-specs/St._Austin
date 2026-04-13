import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'SIH - Systeme d\'Information Hospitalier',
  description: 'Systeme de Gestion Hospitaliere - Cameroun',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return children;
}
