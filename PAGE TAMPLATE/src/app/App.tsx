import { useState } from 'react';
import { TemplateGalleryPage } from '@/app/components/template-gallery-page';
import { TemplateCustomizationPage } from '@/app/components/template-customization-page';
import { Toaster } from '@/app/components/ui/sonner';

type Page = 'gallery' | 'customize';

export default function App() {
  const [currentPage, setCurrentPage] = useState<Page>('gallery');
  const [selectedTemplateId, setSelectedTemplateId] = useState<string | null>(null);

  const handleCustomizeTemplate = (templateId: string) => {
    setSelectedTemplateId(templateId);
    setCurrentPage('customize');
  };

  const handleBackToGallery = () => {
    setCurrentPage('gallery');
    setSelectedTemplateId(null);
  };

  return (
    <>
      {currentPage === 'gallery' && (
        <TemplateGalleryPage onCustomizeTemplate={handleCustomizeTemplate} />
      )}

      {currentPage === 'customize' && selectedTemplateId && (
        <TemplateCustomizationPage
          templateId={selectedTemplateId}
          onBack={handleBackToGallery}
        />
      )}

      <Toaster />
    </>
  );
}