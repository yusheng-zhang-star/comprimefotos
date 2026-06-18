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
      return new Response(JSON.stringify({ ok: false, error: 'missing_fields' }), {
        status: 400, headers: h
      });
    }
  } catch (e) {
    return new Response(JSON.stringify({ ok: false, error: 'parse: ' + e.message }), {
      status: 400, headers: h
    });
  }

  // Send via URLSearchParams (safe in Workers)
  const params = new URLSearchParams();
  params.append('name', name);
  params.append('email', email);
  params.append('_subject', '[ComprimeFotos] ' + (subject || 'General'));
  params.append('message', message);
  params.append('_captcha', 'false');
  params.append('_template', 'table');

  try {
    const fsResp = await fetch('https://formsubmit.co/331728525@qq.com', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: params.toString(),
    });

    const fsBody = await fsResp.text();

    if (fsResp.ok) {
      return new Response(JSON.stringify({ ok: true }), {
        status: 200, headers: h
      });
    }

    return new Response(JSON.stringify({
      ok: false,
      error: 'fs_error',
      status: fsResp.status,
      body: fsBody.substring(0, 200)
    }), { status: 502, headers: h });

  } catch (e) {
    return new Response(JSON.stringify({
      ok: false,
      error: 'fetch_err: ' + (e.message || 'unknown')
    }), { status: 500, headers: h });
  }
}
