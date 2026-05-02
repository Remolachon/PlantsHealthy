import React from 'react';
import { ArrowLeft, Leaf, Camera, Microscope, FileText, Info, Droplets, Sun, Sprout } from 'lucide-react';
import { Header } from '../components/Header';

export const About = ({ onBack, onHomeClick }) => {
  return (
    <>
      {/* We pass an empty function so the header still renders but help button can do nothing or just scroll to top */}
      <Header onHelpClick={() => window.scrollTo(0, 0)} onHomeClick={onHomeClick} />
      <main className="w-full pt-[88px] pb-[100px] px-4 flex flex-col gap-8 max-w-3xl mx-auto">
        <div className="flex items-center gap-2 pt-4">
          <button 
            onClick={onBack}
            className="w-10 h-10 rounded-full bg-[#78A87B]/10 flex items-center justify-center text-[#2C4A2E] dark:text-[#78A87B] hover:bg-[#78A87B]/20 transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>
          <h2 className="font-bold text-[24px] leading-8 text-gray-900 dark:text-gray-100">About & Tutorial</h2>
        </div>
        
        <section className="flex flex-col gap-8">
          {/* Intro block */}
          <div className="bg-[#78A87B] rounded-2xl p-6 shadow-md text-white">
            <h3 className="font-bold text-xl mb-3 flex items-center gap-2">
              <Leaf className="w-6 h-6 text-white" />
              What is PlantsHealthy?
            </h3>
            <p className="leading-relaxed text-white/90">
              PlantsHealthy is an advanced AI application designed to help you monitor and diagnose the health of your plants. Our model can detect various diseases and provide actionable insights just from a simple photo. Maintain your garden, farm, or house plants in optimal condition.
            </p>
          </div>

          {/* How to use */}
          <div>
            <h3 className="font-bold text-[22px] text-gray-900 dark:text-gray-100 mb-5 flex items-center gap-2">
              <Info className="w-6 h-6 text-[#2C4A2E] dark:text-[#78A87B]" />
              How to use the app
            </h3>
            
            <div className="flex flex-col gap-4">
              <div className="flex gap-4 items-start bg-[#F4F9F5] dark:bg-[#1A2E1D] p-5 rounded-2xl shadow-sm border border-[#78A87B]/30">
                <div className="w-12 h-12 rounded-full bg-[#78A87B]/20 flex items-center justify-center shrink-0">
                  <Camera className="w-6 h-6 text-[#2C4A2E] dark:text-[#8cc28f]" />
                </div>
                <div>
                  <h4 className="font-bold text-[#1f3821] dark:text-[#e4f0e5] text-lg">1. Take a clear photo</h4>
                  <p className="text-[#3b5e40] dark:text-[#b5ceb7] mt-1 leading-relaxed">Make sure the leaf or stem is well-lit and in focus. Avoid blurry, dark, or cluttered images for the best analysis results.</p>
                </div>
              </div>

              <div className="flex gap-4 items-start bg-[#F4F9F5] dark:bg-[#1A2E1D] p-5 rounded-2xl shadow-sm border border-[#78A87B]/30">
                <div className="w-12 h-12 rounded-full bg-[#78A87B]/20 flex items-center justify-center shrink-0">
                  <Microscope className="w-6 h-6 text-[#2C4A2E] dark:text-[#8cc28f]" />
                </div>
                <div>
                  <h4 className="font-bold text-[#1f3821] dark:text-[#e4f0e5] text-lg">2. Upload & Analyze</h4>
                  <p className="text-[#3b5e40] dark:text-[#b5ceb7] mt-1 leading-relaxed">Select the photo from your device and click "Analyze Health". Our specialized AI will scan the image for diseases and abnormalities.</p>
                </div>
              </div>

              <div className="flex gap-4 items-start bg-[#F4F9F5] dark:bg-[#1A2E1D] p-5 rounded-2xl shadow-sm border border-[#78A87B]/30">
                <div className="w-12 h-12 rounded-full bg-[#78A87B]/20 flex items-center justify-center shrink-0">
                  <FileText className="w-6 h-6 text-[#2C4A2E] dark:text-[#8cc28f]" />
                </div>
                <div>
                  <h4 className="font-bold text-[#1f3821] dark:text-[#e4f0e5] text-lg">3. Review Results</h4>
                  <p className="text-[#3b5e40] dark:text-[#b5ceb7] mt-1 leading-relaxed">Get an instant diagnosis. The application will highlight healthy and diseased areas, giving you detailed information on how to proceed.</p>
                </div>
              </div>
            </div>
          </div>

          {/* Plant Care Tips */}
          <div>
            <h3 className="font-bold text-[22px] text-gray-900 dark:text-gray-100 mb-5 flex items-center gap-2">
              <Sprout className="w-6 h-6 text-[#2C4A2E] dark:text-[#78A87B]" />
              General Plant Care Tips
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-white dark:bg-[#223B26] p-5 rounded-2xl shadow-sm border-l-4 border-l-[#3b82f6] border border-outline-variant/10">
                <h4 className="font-bold text-[#1f3821] dark:text-[#e4f0e5] flex items-center gap-2">
                  <Droplets className="w-5 h-5 text-[#3b82f6]" /> Water Wisely
                </h4>
                <p className="text-[#3b5e40] dark:text-[#b5ceb7] text-sm mt-2">
                  Overwatering is the #1 killer of house plants. Always check the top 2 inches of soil; only water if it feels dry to the touch. Ensure pots have proper drainage.
                </p>
              </div>

              <div className="bg-white dark:bg-[#223B26] p-5 rounded-2xl shadow-sm border-l-4 border-l-[#eab308] border border-outline-variant/10">
                <h4 className="font-bold text-[#1f3821] dark:text-[#e4f0e5] flex items-center gap-2">
                  <Sun className="w-5 h-5 text-[#eab308]" /> Proper Lighting
                </h4>
                <p className="text-[#3b5e40] dark:text-[#b5ceb7] text-sm mt-2">
                  Match your plant to the right window. Succulents love direct sun (South), while tropicals usually prefer bright, indirect light (East or West).
                </p>
              </div>

              <div className="bg-white dark:bg-[#223B26] p-5 rounded-2xl shadow-sm border-l-4 border-l-[#78A87B] border border-outline-variant/10 md:col-span-2">
                <h4 className="font-bold text-[#1f3821] dark:text-[#e4f0e5] flex items-center gap-2">
                  <Leaf className="w-5 h-5 text-[#78A87B]" /> Routine Inspection
                </h4>
                <p className="text-[#3b5e40] dark:text-[#b5ceb7] text-sm mt-2">
                  Regularly wipe leaves with a damp cloth to remove dust and allow the plant to breathe. Take this time to check the undersides of leaves for any pests or early signs of disease.
                </p>
              </div>
            </div>
          </div>
        </section>
      </main>
    </>
  );
};
