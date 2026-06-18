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
    const resp = await fetch('https://httpbin.org/post', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: 'test=1'
    });
    const text = await resp.text();
    return new Response(JSON.stringify({ ok: true, s: 'fetch_worked', status: resp.status, len: text.length }), { status: 200, headers: h });
  } catch (e) {
    return new Response(JSON.stringify({ ok: false, s: 'crash', error: String(e.message || e).substring(0, 300) }), { status: 500, headers: h });
  }
}
