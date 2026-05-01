import React from 'react';
import { ChevronRight } from 'lucide-react';

export const ResultCard = ({ leaf }) => {
  const isHealthy = leaf.label.toLowerCase() === 'healthy';
  const confidencePercent = (leaf.confidence * 100).toFixed(1);

  return (
    <div className={`bg-surface-container-lowest border rounded-lg p-3 flex items-center gap-3 shadow-sm hover:bg-surface-container transition-colors cursor-pointer
      ${isHealthy ? 'border-outline-variant/30' : 'border-error/30'}`}>
      
      <div className="flex-1 flex flex-col justify-center">
        <div className="flex items-center gap-1.5">
          <span className={`w-2 h-2 rounded-full ${isHealthy ? 'bg-secondary-fixed' : 'bg-error'}`}></span>
          <span className={`font-semibold text-[14px] ${isHealthy ? 'text-on-surface' : 'text-error'}`}>
            {isHealthy ? 'Healthy Segment' : 'Disease Detected'}
          </span>
        </div>
        <span className="font-medium text-[12px] text-on-surface-variant mt-0.5">
          Confidence: {confidencePercent}%
        </span>
        <span className="font-medium text-[11px] text-outline mt-0.5">
          Location: [{leaf.bbox.join(', ')}]
        </span>
      </div>
      <ChevronRight className="w-5 h-5 text-on-surface-variant" />
    </div>
  );
};
