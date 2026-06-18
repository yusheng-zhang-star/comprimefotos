export async function onRequest(context) {
  const h = {
    'Access-Control-Allow-Origin': 'https://comprimefotos.com',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Content-Type': 'application/json'
  };
  if (context.request.method === 'OPTIONS') return new Response(null, { status: 204, headers: h });
  
  try {
    const fd = await context.request.formData();
    const name = fd.get('name') || '';
    const email = fd.get('email') || '';
    const subject = fd.get('subject') || '';
    const message = fd.get('message') || '';
    if (!name || !email || !message) {
      return new Response(JSON.stringify({ ok: false, s: 'validation' }), { status: 400, headers: h });
    }
    
    const plain = 'Nombre: ' + name + '
Correo: ' + email + '
Asunto: ' + subject + '

' + message;
    
    const mcResp = await fetch('https://api.mailchannels.net/tx/v1/send', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        personalizations: [{ to: [{ email: '331728525@qq.com' }] }],
        from: { email: 'noreply@comprimefotos.com', name: 'ComprimeFotos' },
        reply_to: { email: email, name: name },
        subject: '[Formulario] ' + (subject || 'Sin asunto') + ' - ' + name,
        content: [{ type: 'text/plain', value: plain }],
      }),
    });
    
    const mcBody = await mcResp.text();
    
    if (mcResp.ok) {
      return new Response(JSON.stringify({ ok: true, s: 'sent' }), { status: 200, headers: h });
    }
    
    return new Response(JSON.stringify({
      ok: false, s: 'mc_error',
      status: mcResp.status,
      body: mcBody.substring(0, 500)
    }), { status: 502, headers: h });
    
  } catch (e) {
    return new Response(JSON.stringify({
      ok: false, s: 'crash',
      error: String(e.message || e).substring(0, 300)
    }), { status: 500, headers: h });
  }
}
