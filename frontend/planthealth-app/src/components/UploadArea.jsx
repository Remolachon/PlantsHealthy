import React, { useRef, useState } from 'react';
import { Camera, ImagePlus } from 'lucide-react';
import { Camera as CapCamera, CameraResultType, CameraSource } from '@capacitor/camera';
import { Capacitor } from '@capacitor/core';

export const UploadArea = ({ onImageSelect }) => {
  const fileInputRef = useRef(null);
  const [isDragging, setIsDragging] = useState(false);

  const handleNativeCamera = async () => {
    if (Capacitor.isNativePlatform()) {
      try {
        const image = await CapCamera.getPhoto({
          quality: 90,
          allowEditing: false,
          resultType: CameraResultType.Uri,
          source: CameraSource.Prompt // Prompts user to choose Camera or Gallery
        });
        
        if (image.webPath) {
          // Convert the webPath to a File object to keep it consistent with web upload
          const response = await fetch(image.webPath);
          const blob = await response.blob();
          const file = new File([blob], "camera_image.jpg", { type: "image/jpeg" });
          onImageSelect(file, image.webPath);
        }
      } catch (error) {
        console.error("Camera error:", error);
      }
    } else {
      fileInputRef.current?.click();
    }
  };

  const onFileChange = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      const previewUrl = URL.createObjectURL(file);
      onImageSelect(file, previewUrl);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files?.[0];
    if (file && file.type.startsWith('image/')) {
      const previewUrl = URL.createObjectURL(file);
      onImageSelect(file, previewUrl);
    }
  };

  return (
    <section 
      className={`relative group cursor-pointer w-full rounded-[1.5rem] backdrop-blur-xl border-2 border-dashed transition-colors duration-300 flex flex-col items-center justify-center py-12 px-6 text-center gap-4 shadow-[0_8px_32px_0_rgba(6,95,70,0.03)]
      ${isDragging ? 'border-primary bg-surface-container dark:bg-[#1a2b1c]/80 dark:border-[#78A87B]' : 'border-outline-variant/60 bg-surface-container/50 hover:border-primary-fixed-dim hover:bg-surface-container dark:border-white/20 dark:bg-[#1a2b1c]/30 dark:hover:bg-[#1a2b1c]/60 dark:hover:border-[#78A87B]/60'}`}
      onClick={handleNativeCamera}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
    >
      <input 
        type="file" 
        ref={fileInputRef} 
        onChange={onFileChange} 
        accept="image/*" 
        className="hidden" 
      />
      
      <div className="w-16 h-16 rounded-full bg-primary-container/10 flex items-center justify-center mb-3 group-hover:scale-110 transition-transform duration-300">
        {Capacitor.isNativePlatform() ? (
          <Camera className="w-8 h-8 text-primary" />
        ) : (
          <ImagePlus className="w-8 h-8 text-primary" />
        )}
      </div>
      <div className="flex flex-col gap-1">
        <span className="font-semibold text-[20px] leading-7 text-primary dark:text-[#a6f2d1]">
          Click to capture or upload image
        </span>
        <span className="font-semibold text-[14px] leading-5 tracking-[0.01em] text-outline dark:text-gray-400">
          Supports JPG, PNG up to 10MB
        </span>
      </div>
    </section>
  );
};
