/**
 * ComprimeFotos Contact Form Handler (DIAGNOSTIC v2)
 * Catches all errors and returns them for debugging.
 */
export async function onRequest(context) {
  const corsHeaders = {
    'Access-Control-Allow-Origin': 'https://comprimefotos.com',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400',
  };

  if (context.request.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: corsHeaders });
  }

  if (context.request.method !== 'POST') {
    return new Response(JSON.stringify({ ok: false, stage: 'method_check', error: 'not POST' }), {
      status: 405, headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });
  }

  let name, email, subject, message;

  try {
    const ct = context.request.headers.get('Content-Type') || '';
    if (ct.includes('application/json')) {
      const json = await context.request.json();
      name = json.name || ''; email = json.email || ''; subject = json.subject || ''; message = json.message || '';
    } else {
      const fd = await context.request.formData();
      name = fd.get('name') || ''; email = fd.get('email') || ''; subject = fd.get('subject') || ''; message = fd.get('message') || '';
    }

    if (!name || !email || !message) {
      return new Response(JSON.stringify({ ok: false, stage: 'validation', error: 'missing fields' }), {
        status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }
  } catch (e) {
    return new Response(JSON.stringify({ ok: false, stage: 'parse_body', error: e.message }), {
      status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });
  }

  // Step 2: Try MailChannels
  try {
    const mcResp = await fetch('https://api.mailchannels.net/tx/v1/send', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        personalizations: [{ to: [{ email: '331728525@qq.com', name: 'Admin' }] }],
        from: { email: 'noreply@comprimefotos.com', name: 'ComprimeFotos' },
        reply_to: { email: email, name: name },
        subject: '[Formulario] ' + (subject || 'Sin asunto') + ' — ' + name,
        content: [{
          type: 'text/plain',
          value: [
            'Nombre: ' + name,
            'Correo: ' + email,
            'Asunto: ' + subject,
            '',
            '--- Mensaje ---',
            message,
            '',
            '---',
            'Enviado desde: https://comprimefotos.com/contacto',
            'Fecha: ' + new Date().toISOString()
          ].join('\n')
        }],
      }),
    });

    const mcText = await mcResp.text();

    if (mcResp.ok) {
      return new Response(JSON.stringify({ ok: true, message: 'sent' }), {
        status: 200, headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }

    // MailChannels returned error
    return new Response(JSON.stringify({
      ok: false, stage: 'mailchannels',
      error: 'MC returned ' + mcResp.status,
      detail: mcText.substring(0, 500)
    }), { status: 502, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });

  } catch (e) {
    return new Response(JSON.stringify({
      ok: false, stage: 'mailchannels_call',
      error: e.message || 'Unknown fetch error'
    }), { status: 502, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });
  }
}
