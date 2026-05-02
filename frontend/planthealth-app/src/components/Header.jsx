import React from 'react';
import { Leaf, HelpCircle, Home } from 'lucide-react';

export const Header = ({ onHelpClick, onHomeClick }) => {
  return (
    <>
      {/* TopAppBar */}
      <header className="bg-[#78A87B]/95 dark:bg-[#2C4A2E]/95 backdrop-blur-md fixed top-0 left-0 w-full z-50 border-b border-[#628f64]/30 shadow-sm flex justify-between items-center px-6 py-3 transition-colors duration-300">
        <button 
          onClick={onHomeClick}
          className="flex items-center gap-2 hover:opacity-80 transition-opacity text-left"
        >
          <Leaf className="text-white w-6 h-6 shrink-0" />
          <span className="font-semibold tracking-tight text-xl font-black text-white">
            PlantsHealthy
          </span>
        </button>
        <button onClick={onHelpClick} className="w-8 h-8 rounded-full bg-white/20 flex items-center justify-center overflow-hidden border border-white/30 backdrop-blur-sm hover:bg-white/30 transition-colors">
          <HelpCircle className="text-white w-5 h-5" />
        </button>
      </header>

    </>
  );
};
