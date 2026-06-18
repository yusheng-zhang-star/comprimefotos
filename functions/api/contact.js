export async function onRequest(context) {
  const h = {
    'Access-Control-Allow-Origin': 'https://comprimefotos.com',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Content-Type': 'application/json'
  };

  if (context.request.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: h });
  }

  if (context.request.method !== 'POST') {
    return new Response(JSON.stringify({ ok: false, error: 'Method not allowed' }), {
      status: 405, headers: h
    });
  }

  let name, email, subject, message;

  try {
    const ct = context.request.headers.get('Content-Type') || '';
    if (ct.includes('application/json')) {
      const json = await context.request.json();
      name = json.name || '';
      email = json.email || '';
      subject = json.subject || '';
      message = json.message || '';
    } else {
      const fd = await context.request.formData();
      name = fd.get('name') || '';
      email = fd.get('email') || '';
      subject = fd.get('subject') || '';
      message = fd.get('message') || '';
    }

    if (!name || !email || !message) {
      return new Response(JSON.stringify({ ok: false, error: 'Faltan campos obligatorios' }), {
        status: 400, headers: h
      });
    }
  } catch (e) {
    return new Response(JSON.stringify({ ok: false, error: 'Error al procesar los datos' }), {
      status: 400, headers: h
    });
  }

  // Send via FormSubmit.co AJAX endpoint (better Workers compatibility)
  try {
    const payload = new URLSearchParams();
    payload.append('name', name);
    payload.append('email', email);
    payload.append('_subject', '[ComprimeFotos] ' + (subject || 'General'));
    payload.append('message', [
      'Nombre: ' + name,
      'Correo: ' + email,
      'Asunto: ' + (subject || 'General'),
      '',
      '--- Mensaje ---',
      message,
      '',
      '---',
      'Enviado desde: https://comprimefotos.com/contacto'
    ].join('\n'));
    payload.append('_captcha', 'false');
    payload.append('_template', 'table');

    // Try AJAX endpoint first (better for server-side)
    let resp = await fetch('https://formsubmit.co/ajax/331728525@qq.com', {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
      },
      body: payload.toString(),
    });

    // If AJAX fails, try regular endpoint as fallback
    if (!resp.ok) {
      resp = await fetch('https://formsubmit.co/331728525@qq.com', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: payload.toString(),
      });
    }

    if (resp.ok) {
      return new Response(JSON.stringify({ ok: true }), {
        status: 200, headers: h
      });
    }

    // Log the response for debugging
    const respText = await resp.text();
    console.error('FormSubmit error:', resp.status, respText.substring(0, 200));

    return new Response(JSON.stringify({
      ok: false,
      error: 'Error al enviar. Intenta de nuevo mas tarde.'
    }), { status: 500, headers: h });

  } catch (e) {
    console.error('FormSubmit exception:', e.message);
    return new Response(JSON.stringify({
      ok: false,
      error: 'Error de conexion. Intenta de nuevo mas tarde.'
    }), { status: 500, headers: h });
  }
}