function parseCookies(cookie) {
    return cookie.split("; ").map(x=>x.split("=")).reduce((acc,v)=>{acc[v[0]]=v[1];return acc},{});
}

export default function auth({ next, router }) {
    const session = parseCookies(document.cookie).session;
    if (session === undefined) {
      return router.push({ name: 'login' });
    }
    return next();
}