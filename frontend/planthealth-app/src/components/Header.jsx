import React from 'react';
import { Leaf, User, Home, History, Users, Settings } from 'lucide-react';

export const Header = () => {
  return (
    <>
      {/* TopAppBar */}
      <header className="bg-white/70 dark:bg-slate-900/70 backdrop-blur-xl fixed top-0 left-0 w-full z-50 border-b border-primary/10 shadow-[0_4px_20px_-4px_rgba(6,95,70,0.08)] flex justify-between items-center px-6 py-3">
        <div className="flex items-center gap-2">
          <Leaf className="text-primary-container w-6 h-6" />
          <span className="font-semibold tracking-tight text-xl font-black text-primary-container">
            PhytoScan AI
          </span>
        </div>
        <div className="w-8 h-8 rounded-full bg-surface-variant flex items-center justify-center overflow-hidden border border-outline-variant">
          <User className="text-on-surface-variant w-5 h-5" />
        </div>
      </header>

      {/* BottomNavBar (Mobile Only) */}
      <nav className="md:hidden bg-white/80 dark:bg-slate-900/80 backdrop-blur-2xl fixed bottom-0 left-0 w-full z-50 rounded-t-3xl border-t border-white/20 shadow-[0_-10px_30px_-5px_rgba(6,95,70,0.1)] flex justify-around items-center px-4 pb-6 pt-3">
        {/* Home (Active) */}
        <a className="flex flex-col items-center justify-center text-primary-container bg-primary-container/10 rounded-2xl px-5 py-1 scale-90 duration-200" href="#">
          <Home className="w-6 h-6" />
          <span className="text-[11px] font-medium mt-1">Home</span>
        </a>
        {/* History (Inactive) */}
        <a className="flex flex-col items-center justify-center text-outline px-5 py-1 hover:text-primary transition-colors" href="#">
          <History className="w-6 h-6" />
          <span className="text-[11px] font-medium mt-1">History</span>
        </a>
        {/* Community (Inactive) */}
        <a className="flex flex-col items-center justify-center text-outline px-5 py-1 hover:text-primary transition-colors" href="#">
          <Users className="w-6 h-6" />
          <span className="text-[11px] font-medium mt-1">Community</span>
        </a>
        {/* Settings (Inactive) */}
        <a className="flex flex-col items-center justify-center text-outline px-5 py-1 hover:text-primary transition-colors" href="#">
          <Settings className="w-6 h-6" />
          <span className="text-[11px] font-medium mt-1">Settings</span>
        </a>
      </nav>
    </>
  );
};
