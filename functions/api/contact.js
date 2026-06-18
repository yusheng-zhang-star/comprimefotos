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

  try {
    let name, email, subject, message;

    const ct = context.request.headers.get('Content-Type') || '';
    if (ct.includes('application/json')) {
      const json = await context.request.json();
      name = json.name || ''; email = json.email || ''; subject = json.subject || ''; message = json.message || '';
    } else {
      const fd = await context.request.formData();
      name = fd.get('name') || ''; email = fd.get('email') || ''; subject = fd.get('subject') || ''; message = fd.get('message') || '';
    }

    if (!name || !email || !message) {
      return new Response(JSON.stringify({ ok: false, error: 'Faltan campos obligatorios' }), {
        status: 400, headers: h
      });
    }

    // Forward to FormSubmit.co (server-to-server, no CORS issues)
    const fd2 = new FormData();
    fd2.append('name', name);
    fd2.append('email', email);
    fd2.append('_subject', '[ComprimeFotos] ' + (subject || 'General'));
    fd2.append('message', message);
    fd2.append('_captcha', 'false');
    fd2.append('_template', 'table');

    const fsResp = await fetch('https://formsubmit.co/331728525@qq.com', {
      method: 'POST',
      body: fd2,
    });

    if (fsResp.ok) {
      return new Response(JSON.stringify({ ok: true }), {
        status: 200, headers: h
      });
    }

    return new Response(JSON.stringify({
      ok: false,
      error: 'FormSubmit error ' + fsResp.status,
      detail: (await fsResp.text()).substring(0, 300)
    }), { status: 502, headers: h });

  } catch (e) {
    return new Response(JSON.stringify({
      ok: false,
      error: (e.message || 'Unknown error').substring(0, 300)
    }), { status: 500, headers: h });
  }
}
