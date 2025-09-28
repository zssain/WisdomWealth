// Vercel Serverless Function - API Proxy to FastAPI
export default async function handler(req, res) {
  // Enable CORS
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,POST,PUT');
  res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept, Authorization');

  // Handle preflight requests
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  // Only allow POST requests
  if (req.method !== 'POST') {
    return res.status(405).json({ 
      error: 'Method not allowed',
      message: 'Only POST requests are supported'
    });
  }

  try {
    // Validate request body
    const { user_id, text, meta } = req.body;
    
    if (!user_id || typeof user_id !== 'string') {
      return res.status(400).json({
        error: 'Invalid user_id',
        message: 'user_id is required and must be a string'
      });
    }
    
    if (!text || typeof text !== 'string' || text.trim().length === 0) {
      return res.status(400).json({
        error: 'Invalid text',
        message: 'text is required and must be a non-empty string'
      });
    }
    
    if (text.length > 3000) {
      return res.status(400).json({
        error: 'Text too long',
        message: 'text must be less than 3000 characters'
      });
    }

    // Get FastAPI URL from environment
    const fastApiUrl = process.env.FASTAPI_URL;
    if (!fastApiUrl) {
      console.error('FASTAPI_URL environment variable not set');
      return res.status(500).json({
        error: 'Configuration error',
        message: 'Backend service not configured'
      });
    }

    // Forward request to FastAPI
    const response = await fetch(`${fastApiUrl}/route`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        user_id,
        text,
        meta: meta || {}
      })
    });

    // Handle FastAPI response
    if (!response.ok) {
      console.error(`FastAPI error: ${response.status} ${response.statusText}`);
      
      let errorMessage = 'Backend service error';
      try {
        const errorData = await response.json();
        errorMessage = errorData.detail || errorData.message || errorMessage;
      } catch (e) {
        // Ignore JSON parse errors for error responses
      }
      
      return res.status(500).json({
        error: 'Backend error',
        message: errorMessage
      });
    }

    const data = await response.json();
    
    // Validate and sanitize response
    const sanitizedResponse = {
      response: data.response || 'No response from agents',
      risk: data.risk || 'low',
      agent_traces: Array.isArray(data.agent_traces) ? data.agent_traces : [],
      actions: Array.isArray(data.actions) ? data.actions : [],
      logs_id: data.logs_id || null,
      confidence_score: typeof data.confidence_score === 'number' ? data.confidence_score : null,
      timestamp: data.timestamp || new Date().toISOString(),
      family_alert_id: data.family_alert_id || null
    };

    return res.status(200).json(sanitizedResponse);

  } catch (error) {
    console.error('API route error:', error);
    
    return res.status(500).json({
      error: 'Internal server error',
      message: 'An unexpected error occurred. Please try again.'
    });
  }
}