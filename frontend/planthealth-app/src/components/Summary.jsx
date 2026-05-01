import React from 'react';
import { Leaf, Bug } from 'lucide-react';

export const Summary = ({ healthy, diseased }) => {
  return (
    <section className="grid grid-cols-2 gap-4">
      {/* Healthy Card */}
      <div className="bg-surface-container-lowest border border-outline-variant/30 rounded-xl p-4 flex flex-col gap-2 relative overflow-hidden shadow-sm">
        <div className="absolute top-0 right-0 w-24 h-24 bg-primary-fixed/20 rounded-full blur-2xl -mr-8 -mt-8"></div>
        <div className="flex items-center gap-1 text-primary">
          <Leaf className="w-5 h-5" />
          <span className="font-semibold text-[14px]">Healthy</span>
        </div>
        <div className="font-bold text-[32px] leading-10 text-primary-container">{healthy || 0}</div>
        <span className="font-medium text-[12px] text-on-surface-variant">Leaves clear</span>
      </div>

      {/* Diseased Card */}
      <div className="bg-error-container/30 border border-error/20 rounded-xl p-4 flex flex-col gap-2 relative overflow-hidden shadow-sm">
        <div className="absolute top-0 right-0 w-24 h-24 bg-error/10 rounded-full blur-2xl -mr-8 -mt-8"></div>
        <div className="flex items-center gap-1 text-error">
          <Bug className="w-5 h-5" />
          <span className="font-semibold text-[14px]">Diseased</span>
        </div>
        <div className="font-bold text-[32px] leading-10 text-error">{diseased || 0}</div>
        <span className="font-medium text-[12px] text-on-surface-variant">Require attention</span>
      </div>
    </section>
  );
};
