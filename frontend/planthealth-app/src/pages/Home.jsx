import React, { useState } from 'react';
import { UploadArea } from '../components/UploadArea';
import { Microscope } from 'lucide-react';
import { Header } from '../components/Header';
import { ImagePreview } from '../components/ImagePreview';

export const Home = ({ onAnalyze }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);

  const handleImageSelect = (file, url) => {
    setSelectedFile(file);
    setPreviewUrl(url);
  };

  const handleAnalyzeClick = () => {
    if (selectedFile && previewUrl) {
      onAnalyze(selectedFile, previewUrl);
    }
  };

  return (
    <>
      <Header />
      <main className="w-full pt-[88px] pb-[100px] px-4 max-w-2xl mx-auto flex flex-col gap-6">
        <section className="flex flex-col gap-1 pt-4">
          <h1 className="font-bold text-[32px] leading-10 text-on-background">Analyze Plant</h1>
          <p className="text-[16px] leading-6 text-on-surface-variant">
            Upload a clear photo of the affected plant leaves or stem for an instant AI health assessment.
          </p>
        </section>

        {!selectedFile ? (
          <UploadArea onImageSelect={handleImageSelect} />
        ) : (
          <div className="flex flex-col gap-4">
            <ImagePreview imageUrl={previewUrl} />
            <button 
              onClick={() => { setSelectedFile(null); setPreviewUrl(null); }}
              className="text-primary font-medium text-sm self-end hover:underline"
            >
              Choose another image
            </button>
          </div>
        )}

        <section className="pt-3">
          <button 
            disabled={!selectedFile}
            onClick={handleAnalyzeClick}
            className={`w-full rounded-full py-4 font-semibold text-[20px] flex justify-center items-center gap-2 transition-all shadow-sm
              ${selectedFile 
                ? 'bg-primary text-on-primary hover:bg-primary-container shadow-[0_4px_15px_-3px_rgba(6,95,70,0.3)]' 
                : 'bg-tertiary-fixed-dim text-on-tertiary-fixed opacity-60 cursor-not-allowed'}`}
          >
            <Microscope className="w-6 h-6" />
            Analyze Health
          </button>
          {!selectedFile && (
            <p className="text-center font-medium text-[12px] text-outline mt-3">
              Select an image to enable analysis.
            </p>
          )}
        </section>
      </main>
    </>
  );
};
