// src/utils/apiDiagnostics.ts

/**
 * Test connectivity to the backend API
 */
export async function testBackendConnection(apiBase: string): Promise<{
  success: boolean;
  message: string;
  details: any;
}> {
  try {
    console.log('🔍 Testing backend connection to:', apiBase);
    
    const response = await fetch(`${apiBase}/api/shop/products/`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
    });
    
    const corsHeaders = {
      'access-control-allow-origin': response.headers.get('access-control-allow-origin'),
      'access-control-allow-credentials': response.headers.get('access-control-allow-credentials'),
      'content-type': response.headers.get('content-type'),
    };
    
    console.log('✅ Backend connection successful');
    console.log('📋 CORS Headers:', corsHeaders);
    
    return {
      success: response.ok,
      message: `Connected successfully (status: ${response.status})`,
      details: {
        status: response.status,
        corsHeaders,
        url: `${apiBase}/api/shop/products/`,
      },
    };
  } catch (error: any) {
    if (error instanceof TypeError && error.message === 'Failed to fetch') {
      console.error('❌ Network error - Backend not accessible');
      return {
        success: false,
        message: `Cannot reach backend at ${apiBase}`,
        details: {
          error: 'Failed to fetch',
          type: 'NETWORK_ERROR',
          apiBase,
          suggestion: 'Make sure Django backend is running on ' + apiBase,
        },
      };
    }
    
    return {
      success: false,
      message: error.message,
      details: {
        error: error.toString(),
        type: 'UNKNOWN_ERROR',
      },
    };
  }
}

/**
 * Test API endpoint with detailed CORS and error information
 */
export async function testApiEndpoint(
  endpoint: string,
  method: string = 'GET',
  body?: any
): Promise<{
  success: boolean;
  status?: number;
  corsHeaders: any;
  error?: string;
  responseBody?: any;
}> {
  try {
    const apiBase = import.meta.env.VITE_API_BASE || 'http://localhost:8000';
    const url = `${apiBase}${endpoint}`;
    
    console.log(`🔍 Testing ${method} ${url}`);
    
    const response = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: body ? JSON.stringify(body) : undefined,
      credentials: 'include',
    });
    
    const corsHeaders = {
      'access-control-allow-origin': response.headers.get('access-control-allow-origin'),
      'access-control-allow-credentials': response.headers.get('access-control-allow-credentials'),
      'access-control-allow-methods': response.headers.get('access-control-allow-methods'),
      'content-type': response.headers.get('content-type'),
    };
    
    let responseBody: any = null;
    try {
      responseBody = await response.json();
    } catch {
      responseBody = await response.text();
    }
    
    return {
      success: response.ok,
      status: response.status,
      corsHeaders,
      responseBody,
    };
  } catch (error: any) {
    return {
      success: false,
      corsHeaders: {},
      error: error.message,
    };
  }
}

/**
 * Generate a detailed diagnostics report
 */
export async function generateDiagnosticsReport(): Promise<string> {
  const apiBase = import.meta.env.VITE_API_BASE || 'http://localhost:8000';
  
  const report: string[] = [
    '═══════════════════════════════════════',
    'API DIAGNOSTICS REPORT',
    '═══════════════════════════════════════',
    `API Base URL: ${apiBase}`,
    `Frontend URL: ${window.location.href}`,
    `User Agent: ${navigator.userAgent}`,
    '',
  ];
  
  // Test connection
  const connTest = await testBackendConnection(apiBase);
  report.push('CONNECTION TEST');
  report.push('-'.repeat(40));
  report.push(`Status: ${connTest.success ? '✅ SUCCESS' : '❌ FAILED'}`);
  report.push(`Message: ${connTest.message}`);
  report.push(`Details: ${JSON.stringify(connTest.details, null, 2)}`);
  report.push('');
  
  // Test signup endpoint
  const signupTest = await testApiEndpoint('/api/users/register/', 'POST', {
    username: 'test',
    email: 'test@example.com',
    password: 'test123',
  });
  report.push('SIGNUP ENDPOINT TEST');
  report.push('-'.repeat(40));
  report.push(`Status: ${signupTest.status}`);
  report.push(`CORS Headers: ${JSON.stringify(signupTest.corsHeaders, null, 2)}`);
  if (signupTest.error) {
    report.push(`Error: ${signupTest.error}`);
  }
  report.push('');
  
  // Test products endpoint
  const productsTest = await testApiEndpoint('/api/shop/products/', 'GET');
  report.push('PRODUCTS ENDPOINT TEST');
  report.push('-'.repeat(40));
  report.push(`Status: ${productsTest.status}`);
  report.push(`CORS Headers: ${JSON.stringify(productsTest.corsHeaders, null, 2)}`);
  if (productsTest.error) {
    report.push(`Error: ${productsTest.error}`);
  }
  report.push('');
  
  report.push('═══════════════════════════════════════');
  
  return report.join('\n');
}
