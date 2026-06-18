/**
 * ComprimeFotos Contact Form Handler
 * Cloudflare Pages Function — handles POST /api/contact
 * Sends form submissions via MailChannels to admin email.
 */

export async function onRequest(context) {
  const { request } = context;

  const corsHeaders = {
    'Access-Control-Allow-Origin': 'https://comprimefotos.com',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400',
  };

  // Handle CORS preflight
  if (request.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: corsHeaders });
  }

  // Only accept POST
  if (request.method !== 'POST') {
    return new Response(
      JSON.stringify({ success: false, message: 'Método no permitido' }),
      { status: 405, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    );
  }

  try {
    let name, email, subject, message;

    // Try JSON first, then FormData
    const contentType = request.headers.get('Content-Type') || '';
    if (contentType.includes('application/json')) {
      const json = await request.json();
      name = json.name || '';
      email = json.email || '';
      subject = json.subject || '';
      message = json.message || '';
    } else {
      const formData = await request.formData();
      name = formData.get('name') || '';
      email = formData.get('email') || '';
      subject = formData.get('subject') || '';
      message = formData.get('message') || '';
    }

    // Basic validation
    if (!name || !email || !message) {
      return new Response(
        JSON.stringify({ success: false, message: 'Faltan campos obligatorios' }),
        { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      );
    }

    // Build plain text email
    const plainText = [
      `Nombre: ${name}`,
      `Correo electrónico: ${email}`,
      `Asunto: ${subject}`,
      '',
      '--- Mensaje ---',
      message,
      '',
      '---',
      `Enviado desde: https://comprimefotos.com/contact`,
      `Fecha: ${new Date().toISOString()}`,
    ].join('\n');

    // Send via MailChannels
    const mcResp = await fetch('https://api.mailchannels.net/tx/v1/send', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        personalizations: [
          { to: [{ email: '331728525@qq.com', name: 'Admin ComprimeFotos' }] },
        ],
        from: {
          email: 'noreply@comprimefotos.com',
          name: 'ComprimeFotos Contacto',
        },
        subject: `[Formulario] ${subject} — ${name}`,
        content: [
          { type: 'text/plain', value: plainText },
        ],
      }),
    });

    if (mcResp.ok) {
      return new Response(
        JSON.stringify({ success: true, message: 'Mensaje enviado correctamente' }),
        { status: 200, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      );
    }

    // MailChannels error
    const mcError = await mcResp.text();
    console.error('MailChannels error:', mcResp.status, mcError.substring(0, 500));

    return new Response(
      JSON.stringify({ success: false, message: 'Error al enviar el mensaje. Intenta de nuevo más tarde.' }),
      { status: 502, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    );

  } catch (err) {
    console.error('Contact handler error:', err.message);
    return new Response(
      JSON.stringify({ success: false, message: 'Error del servidor. Intenta de nuevo más tarde.' }),
      { status: 500, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    );
  }
}
