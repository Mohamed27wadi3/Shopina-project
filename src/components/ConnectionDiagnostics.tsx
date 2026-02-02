// src/components/ConnectionDiagnostics.tsx

import { useEffect, useState } from 'react';
import { testBackendConnection, generateDiagnosticsReport } from '../utils/apiDiagnostics';

export function ConnectionDiagnostics() {
  const [status, setStatus] = useState<'checking' | 'connected' | 'failed'>('checking');
  const [report, setReport] = useState<string>('');
  const apiBase = import.meta.env.VITE_API_BASE || 'http://localhost:8000';

  useEffect(() => {
    const checkConnection = async () => {
      const result = await testBackendConnection(apiBase);
      setStatus(result.success ? 'connected' : 'failed');
      
      if (!result.success) {
        const fullReport = await generateDiagnosticsReport();
        setReport(fullReport);
      }
    };

    checkConnection();
  }, [apiBase]);

  if (status === 'checking') {
    return (
      <div className="flex items-center justify-center p-4">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto mb-2"></div>
          <p className="text-gray-600">Vérification de la connexion au serveur...</p>
        </div>
      </div>
    );
  }

  if (status === 'connected') {
    return null; // Don't show anything if connected
  }

  // Failed connection - show error
  return (
    <div className="fixed inset-0 bg-red-50 border-b-4 border-red-500 p-4 z-50 overflow-auto">
      <div className="max-w-4xl mx-auto">
        <div className="mb-4">
          <h2 className="text-lg font-bold text-red-700">⚠️ Erreur de Connexion</h2>
          <p className="text-red-600 mt-2">
            Le frontend ne peut pas se connecter au backend Django.
          </p>
        </div>

        <div className="bg-white p-4 rounded border border-red-200 mb-4">
          <h3 className="font-bold text-red-700 mb-2">🔧 Diagnostic:</h3>
          <pre className="text-xs overflow-auto bg-gray-100 p-3 rounded whitespace-pre-wrap break-words max-h-60">
            {report}
          </pre>
        </div>

        <div className="bg-blue-50 p-4 rounded border border-blue-200">
          <h3 className="font-bold text-blue-700 mb-2">✅ Solutions:</h3>
          <ul className="text-sm text-blue-600 space-y-2">
            <li>1. Vérifiez que le serveur Django est en cours d'exécution:</li>
            <li className="ml-4">
              <code className="bg-white px-2 py-1 rounded">
                python manage.py runserver
              </code>
            </li>
            <li className="mt-3">2. Assurez-vous que le backend écoute sur: <strong>{apiBase}</strong></li>
            <li className="mt-3">3. Vérifiez CORS dans <code className="bg-white px-2 py-1 rounded">settings.py</code>:</li>
            <li className="ml-4">
              <code className="bg-white px-2 py-1 rounded">
                CORS_ALLOWED_ORIGINS = ['http://localhost:3000', ...]
              </code>
            </li>
            <li className="mt-3">4. Testez manuellement en accédant à:</li>
            <li className="ml-4">
              <a
                href={`${apiBase}/api/shop/products/`}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-500 underline"
              >
                {apiBase}/api/shop/products/
              </a>
            </li>
          </ul>
        </div>

        <div className="mt-4">
          <button
            onClick={() => window.location.reload()}
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
          >
            Réessayer
          </button>
        </div>
      </div>
    </div>
  );
}
