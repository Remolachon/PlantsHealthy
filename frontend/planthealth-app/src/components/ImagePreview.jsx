import React from 'react';

export const ImagePreview = ({ imageUrl, annotatedImageBase64 }) => {
  // If we have an annotated image from the backend, use it. Otherwise use the local preview.
  const displaySrc = annotatedImageBase64 
    ? `data:image/jpeg;base64,${annotatedImageBase64}` 
    : imageUrl;

  return (
    <section className="relative w-full aspect-square md:aspect-video rounded-xl overflow-hidden shadow-sm border border-outline-variant/30 bg-surface-container-lowest">
      {displaySrc ? (
        <img 
          src={displaySrc} 
          alt="Plant scan" 
          className="w-full h-full object-cover"
        />
      ) : (
        <div className="w-full h-full flex items-center justify-center bg-surface-variant text-on-surface-variant">
          No image selected
        </div>
      )}
    </section>
  );
};
