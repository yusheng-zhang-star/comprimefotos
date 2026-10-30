// 全站中间件：主机名归一 + staging 屏蔽 + pt-BR 页面下线
// 1. www.comprimefotos.com → comprimefotos.com（308，保留路径与查询串）
//    _redirects 无法按主机名匹配，必须在中间件里做
// 2. /staging/* 一律 404：草稿页不应对外提供（与 robots.txt 的 Disallow 双保险）
// 3. pt-BR 页面一律 410 Gone：西语站点混入葡语页造成语言混乱信号，已决定永久下线
const RETIRED_PT_PAGES = new Set([
  "/blog/ampliar-imagem-sem-perder-qualidade-gratis",
  "/blog/como-colocar-fundo-branco-foto-produto-gratis",
  "/blog/comprimir-imagem-sem-perder-qualidade-gratis",
  "/blog/converter-png-para-jpg-gratis",
  "/blog/tamanho-foto-mercado-livre-2026",
  "/blog/tamanho-imagem-shopee-brasil-2026",
]);

export async function onRequest(context) {
  const url = new URL(context.request.url);

  if (url.hostname === "www.comprimefotos.com") {
    const target = "https://comprimefotos.com" + url.pathname + url.search;
    return Response.redirect(target, 308);
  }

  if (url.pathname === "/staging" || url.pathname.startsWith("/staging/")) {
    return new Response("Not found", { status: 404 });
  }

  // 兼容带 .html 后缀的旧链接，统一去掉后缀再比对
  const path = url.pathname.replace(/\.html$/, "");
  if (RETIRED_PT_PAGES.has(path)) {
    return new Response("Gone", { status: 410 });
  }

  return context.next();
}
