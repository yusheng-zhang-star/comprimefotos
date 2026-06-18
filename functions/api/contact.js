export async function onRequest(context) {
  return new Response(JSON.stringify({ ok: true, t: Date.now() }), {
    headers: {
      'content-type': 'application/json',
      'access-control-allow-origin': '*'
    }
  });
}
