import React from 'react';
import { ArrowLeft, Download } from 'lucide-react';
import { Header } from '../components/Header';
import { ImagePreview } from '../components/ImagePreview';
import { Summary } from '../components/Summary';
import { ResultCard } from '../components/ResultCard';

export const Result = ({ result, previewUrl, onBack }) => {
  const { summary, leaves, image } = result || {};

  return (
    <>
      <Header />
      <main className="w-full pt-[88px] pb-[100px] px-4 flex flex-col gap-6 max-w-3xl mx-auto">
        {/* Header / Back Context */}
        <div className="flex items-center gap-2 pt-4">
          <button 
            onClick={onBack}
            className="w-10 h-10 rounded-full bg-surface-container flex items-center justify-center text-primary hover:bg-surface-container-high transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>
          <h2 className="font-bold text-[24px] leading-8 text-on-background">Scan Results</h2>
        </div>

        {/* Results Image Container */}
        <ImagePreview imageUrl={previewUrl} annotatedImageBase64={image} />

        {/* Summary Section */}
        {summary && (
          <Summary healthy={summary.healthy} diseased={summary.diseased} />
        )}

        {/* Details Section */}
        <section className="flex flex-col gap-4">
          <h3 className="font-semibold text-[20px] text-on-background">Leaves Detected</h3>
          <div className="flex flex-col gap-2">
            {leaves && leaves.length > 0 ? (
              leaves.map((leaf, index) => (
                <ResultCard key={index} leaf={leaf} />
              ))
            ) : (
              <div className="text-on-surface-variant text-sm p-4 text-center bg-surface-container-lowest rounded-lg border border-outline-variant/30">
                No distinct leaves detected.
              </div>
            )}
          </div>
        </section>

        {/* Action Button */}
        <div className="pt-3 pb-8">
          <button className="w-full bg-primary hover:bg-primary-container text-on-primary font-semibold text-[14px] rounded-full py-4 px-6 flex items-center justify-center gap-2 transition-all shadow-[0_4px_15px_-3px_rgba(6,95,70,0.3)]">
            <Download className="w-5 h-5" />
            Download Full Report
          </button>
        </div>
      </main>
    </>
  );
};
