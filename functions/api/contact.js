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

    // Test 1: formsubmit.co
    const params = new URLSearchParams();
    params.append('name', name);
    params.append('email', email);
    params.append('_subject', 'test');
    params.append('message', message);
    params.append('_captcha', 'false');

    const resp = await fetch('https://formsubmit.co/331728525@qq.com', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: params.toString()
    });

    const text = await resp.text();
    return new Response(JSON.stringify({
      ok: true, s: 'formsubmit',
      status: resp.status,
      text: text.substring(0, 200)
    }), { status: 200, headers: h });

  } catch (e) {
    return new Response(JSON.stringify({
      ok: false, s: 'crash',
      error: String(e.message || e).substring(0, 300)
    }), { status: 500, headers: h });
  }
}
