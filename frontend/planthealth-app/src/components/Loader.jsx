import React from 'react';
import { Loader2 } from 'lucide-react';

export const Loader = ({ message = "Analyzing image..." }) => {
  return (
    <div className="flex flex-col items-center justify-center p-8 gap-4">
      <Loader2 className="w-10 h-10 text-primary animate-spin" />
      <span className="font-semibold text-primary">{message}</span>
    </div>
  );
};
