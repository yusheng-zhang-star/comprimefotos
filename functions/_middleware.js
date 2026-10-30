// 全站中间件：主机名归一 + staging 屏蔽
// 1. www.comprimefotos.com → comprimefotos.com（308，保留路径与查询串）
//    _redirects 无法按主机名匹配，必须在中间件里做
// 2. /staging/* 一律 404：草稿页不应对外提供（与 robots.txt 的 Disallow 双保险）
export async function onRequest(context) {
  const url = new URL(context.request.url);

  if (url.hostname === "www.comprimefotos.com") {
    const target = "https://comprimefotos.com" + url.pathname + url.search;
    return Response.redirect(target, 308);
  }

  if (url.pathname === "/staging" || url.pathname.startsWith("/staging/")) {
    return new Response("Not found", { status: 404 });
  }

  return context.next();
}
