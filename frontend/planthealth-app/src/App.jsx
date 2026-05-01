import React, { useState } from 'react';
import { Home } from './pages/Home';
import { Result } from './pages/Result';
import { usePredict } from './hooks/usePredict';
import { Loader } from './components/Loader';
import { Header } from './components/Header';
import { AlertCircle } from 'lucide-react';

function App() {
  const { analyzeImage, status, result, error, reset } = usePredict();
  const [previewUrl, setPreviewUrl] = useState(null);

  const handleAnalyze = async (file, url) => {
    setPreviewUrl(url);
    await analyzeImage(file);
  };

  const handleBack = () => {
    reset();
    setPreviewUrl(null);
  };

  if (status === 'loading') {
    return (
      <div className="min-h-screen flex flex-col bg-background">
        <Header />
        <main className="flex-1 w-full flex items-center justify-center pt-[88px] pb-[100px]">
          <Loader message="Analyzing plant health..." />
        </main>
      </div>
    );
  }

  if (status === 'error') {
    return (
      <div className="min-h-screen flex flex-col bg-background">
        <Header />
        <main className="flex-1 w-full flex flex-col items-center justify-center p-6 gap-6 pt-[88px] pb-[100px]">
          <AlertCircle className="w-16 h-16 text-error" />
          <div className="text-center">
            <h2 className="font-bold text-xl text-on-background mb-2">Analysis Failed</h2>
            <p className="text-error">{error}</p>
          </div>
          <button 
            onClick={reset}
            className="bg-primary text-on-primary px-6 py-3 rounded-full font-medium mt-4 hover:bg-primary-container"
          >
            Try Again
          </button>
        </main>
      </div>
    );
  }

  if (status === 'success' && result) {
    return <Result result={result} previewUrl={previewUrl} onBack={handleBack} />;
  }

  return <Home onAnalyze={handleAnalyze} />;
}

export default App;
