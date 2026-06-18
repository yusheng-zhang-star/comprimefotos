export async function onRequest(context) {
  const corsHeaders = {
    'Access-Control-Allow-Origin': 'https://comprimefotos.com',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  };
  if (context.request.method === 'OPTIONS') return new Response(null, { status: 204, headers: corsHeaders });
  try {
    const fd = await context.request.formData();
    const name = fd.get('name') || '';
    const email = fd.get('email') || '';
    const subject = fd.get('subject') || '';
    const message = fd.get('message') || '';
    if (!name || !email || !message) {
      return new Response(JSON.stringify({ ok: false, s: 'validation' }), {
        status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }
    return new Response(JSON.stringify({ ok: true, s: 'parsed', name: name, email: email, subject: subject }), {
      status: 200, headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });
  } catch (e) {
    return new Response(JSON.stringify({ ok: false, s: 'error', e: e.message }), {
      status: 500, headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });
  }
}
